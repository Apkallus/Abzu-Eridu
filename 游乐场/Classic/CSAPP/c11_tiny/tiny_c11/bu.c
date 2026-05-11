/* $begin tinymain */
/*
 * tiny.c - A simple, iterative HTTP/1.0 Web server that uses the 
 *     GET method to serve static and dynamic content.
 *
 * Updated 11/2019 droh 
 *   - Fixed sprintf() aliasing issue in serve_static(), and clienterror().
 */

#include "csapp.h"

int is_head=0;

void doit(int fd);
void read_requesthdrs(rio_t *rp);
int parse_uri(char *uri, char *filename, char *cgiargs);
void serve_static(int fd, char *filename, int filesize);
void get_filetype(char *filename, char *filetype);
void serve_dynamic(int fd, char *filename, char *cgiargs);
void clienterror(int fd, char *cause, char *errnum, 
		 char *shortmsg, char *longmsg);

void sigchld_handler(int sig);
void serve_static_malloc(int fd, char *filename, int filesize);
void read_requesthdrs_post(rio_t *rp, char *buf);
void sigpipe_handler(int sig);
int is_alive(int fd);

int main(int argc, char **argv) 
{
    int listenfd, connfd;
    char hostname[MAXLINE], port[MAXLINE];
    socklen_t clientlen;
    struct sockaddr_storage clientaddr;

    //11.8 子进程信号处理 设置信号处理函数
    // 由于此处无需前台等待，于是也无需在fork前阻挡子进程的信号
    Signal(SIGCHLD, sigchld_handler);
    //11.13 SIGPIPE信号处理
    Signal(SIGPIPE, sigpipe_handler);

    /* Check command line args */
    if (argc != 2) {
	fprintf(stderr, "usage: %s <port>\n", argv[0]);
	exit(1);
    }

    listenfd = Open_listenfd(argv[1]);
    while (1) {
	clientlen = sizeof(clientaddr);
	connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen); //line:netp:tiny:accept
        Getnameinfo((SA *) &clientaddr, clientlen, hostname, MAXLINE, 
                    port, MAXLINE, 0);
        printf("Accepted connection from (%s, %s)\n", hostname, port);
    // echo(connfd); 11.6 A. 回显请求报头与请求行
	doit(connfd);                                             //line:netp:tiny:doit
	Close(connfd);                                            //line:netp:tiny:close
    }
}
/* $end tinymain */

// 11.6 A. 回显请求报头与请求行
void echo(int fd){
    size_t n;
    char buf[MAXLINE];
    rio_t rio;

    Rio_readinitb(&rio, fd);
    while((n = Rio_readlineb(&rio, buf, MAXLINE)) !=0 ){
        //@# 应当对报头最后的空行进行处理，否则持续回显
        if(strcmp(buf,"\r\n")==0){
            break;
        }
        rio_writen(fd, buf, n);
    }
}
/*
 * doit - handle one HTTP request/response transaction
 */
/* $begin doit */
void doit(int fd) 
{
    int is_static, is_post;
    struct stat sbuf;
    char buf[MAXLINE], method[MAXLINE], uri[MAXLINE], version[MAXLINE], post_buf[MAXLINE];
    char filename[MAXLINE], cgiargs[MAXLINE];
    rio_t rio;

    /* Read request line and headers */
    Rio_readinitb(&rio, fd);
    if (!Rio_readlineb(&rio, buf, MAXLINE))  //line:netp:doit:readrequest
        return;
    printf("%s", buf);
    sscanf(buf, "%s %s %s", method, uri, version);       //line:netp:doit:parserequest
    // if (strcasecmp(method, "GET")) {                     //line:netp:doit:beginrequesterr
    //11.11支持HEAD方法 
    //HEAD方法只发送头部
    //设置全局变量is_head，检测此变量来决定是否将body输出
    //对于子进程设置环境变量
    is_head=!strcasecmp(method, "HEAD");
    is_post=!strcasecmp(method, "POST");
    //11.12支持POST方法获得动态内容
    if (strcasecmp(method, "GET")&&strcasecmp(method, "HEAD")&&strcasecmp(method, "POST")) {
        clienterror(fd, method, "501", "Not Implemented",
                    "Tiny does not implement this method");
        return;
    }                     
    if(is_post){
        read_requesthdrs_post(&rio, post_buf);
    }else{
        read_requesthdrs(&rio);  
    }                               //line:netp:doit:endrequesterr
                                //line:netp:doit:readrequesthdrs

    /* Parse URI from GET request */
    is_static = parse_uri(uri, filename, cgiargs);       //line:netp:doit:staticcheck
    if (stat(filename, &sbuf) < 0) {                     //line:netp:doit:beginnotfound
	clienterror(fd, filename, "404", "Not found",
		    "Tiny couldn't find this file");
	return;
    }                                                    //line:netp:doit:endnotfound

    if (is_static) { /* Serve static content */          
	if (!(S_ISREG(sbuf.st_mode)) || !(S_IRUSR & sbuf.st_mode)) { //line:netp:doit:readable
	    clienterror(fd, filename, "403", "Forbidden",
			"Tiny couldn't read the file");
	    return;
	}
	serve_static(fd, filename, sbuf.st_size);        //line:netp:doit:servestatic
    //11.9使用malloc\rio_readn\rio_writen复制内容
    // serve_static_malloc(fd, filename, sbuf.st_size); 
    }
    else { /* Serve dynamic content */
	if (!(S_ISREG(sbuf.st_mode)) || !(S_IXUSR & sbuf.st_mode)) { //line:netp:doit:executable
	    clienterror(fd, filename, "403", "Forbidden",
			"Tiny couldn't run the CGI program");
	    return;
	}
    //11.12 POST 调用read_requesthdrs_post将body的参数保存到post_buf
    if(is_post){
        strcpy(cgiargs, post_buf);
    }
	serve_dynamic(fd, filename, cgiargs);            //line:netp:doit:servedynamic
    }
}
/* $end doit */

/*
 * read_requesthdrs - read HTTP request headers
 */
/* $begin read_requesthdrs */
void read_requesthdrs(rio_t *rp) 
{
    char buf[MAXLINE];

    Rio_readlineb(rp, buf, MAXLINE);
    printf("%s", buf);
    while(strcmp(buf, "\r\n")) {          //line:netp:readhdrs:checkterm
        Rio_readlineb(rp, buf, MAXLINE);
        printf("%s", buf);
    }
    return;
}
/* $end read_requesthdrs */

/*
 * parse_uri - parse URI into filename and CGI args
 *             return 0 if dynamic content, 1 if static
 */
/* $begin parse_uri */
int parse_uri(char *uri, char *filename, char *cgiargs) 
{
    char *ptr;

    if (!strstr(uri, "cgi-bin")) {  /* Static content */ //line:netp:parseuri:isstatic
	strcpy(cgiargs, "");                             //line:netp:parseuri:clearcgi
	strcpy(filename, ".");                           //line:netp:parseuri:beginconvert1
	strcat(filename, uri);                           //line:netp:parseuri:endconvert1
	if (uri[strlen(uri)-1] == '/')                   //line:netp:parseuri:slashcheck
	    strcat(filename, "home.html");               //line:netp:parseuri:appenddefault
	return 1;
    }
    else {  /* Dynamic content */                        //line:netp:parseuri:isdynamic
	ptr = index(uri, '?');                           //line:netp:parseuri:beginextract
	if (ptr) {
	    strcpy(cgiargs, ptr+1);
	    *ptr = '\0';
	}
	else 
	    strcpy(cgiargs, "");                         //line:netp:parseuri:endextract
	strcpy(filename, ".");                           //line:netp:parseuri:beginconvert2
	strcat(filename, uri);                           //line:netp:parseuri:endconvert2
	return 0;
    }
}
/* $end parse_uri */

/*
 * serve_static - copy a file back to the client 
 */
/* $begin serve_static */
void serve_static(int fd, char *filename, int filesize)
{
    int srcfd;
    char *srcp, filetype[MAXLINE], buf[MAXBUF], buf_temp[MAXLINE];
    //11.13使用sleep来测试关闭客户端后服务器的响应
    //捕获信号后，打印出2后终止
    //第一次正常，第二次终止，如果捕获则返回-1，并将errno设置为EPIPE
    //那么应当在所有写入都检测返回状态，如果异常则跳过后续写入
    //减少写入次数来减少判断数量,如果将写入减少到2次，则不存在第3次的异常终止
    //虽然服务器能够避免终止，但浏览器仍能够收到乱码的响应
    // for(int i=0;i<5;i++){
    //     sleep(1);
    // }
    /* Send response headers to client */
    get_filetype(filename, filetype);    //line:netp:servestatic:getfiletype
    sprintf(buf, "HTTP/1.0 200 OK\r\n"); //line:netp:servestatic:beginserve
    // printf("1\n");
    // rio_writen(fd, buf, strlen(buf));
    sprintf(buf_temp, "Server: Tiny Web Server\r\n");
    strcpy(buf, buf_temp);
    // printf("2\n"); 
    // rio_writen(fd, buf, strlen(buf));
    sprintf(buf_temp, "Content-length: %d\r\n", filesize);
    strcpy(buf, buf_temp);
    // printf("3\n");
    // rio_writen(fd, buf, strlen(buf));
    sprintf(buf_temp, "Content-type: %s\r\n\r\n", filetype);
    strcpy(buf, buf_temp);
    // printf("4\n");

    int wr=rio_writen(fd, buf, strlen(buf));    //line:netp:servestatic:endserve
    printf("rr=%d %s\n",wr,strerror(errno));
    

    //11.11 HEAD方法不输出body
    if(!is_head){
        /* Send response body to client */
        srcfd = Open(filename, O_RDONLY, 0); //line:netp:servestatic:open
        srcp = Mmap(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0); //line:netp:servestatic:mmap
        wr=rio_writen(fd, srcp, filesize);  
        printf("rr=%d %s\n",wr,strerror(errno));
        Close(srcfd);                       //line:netp:servestatic:close
        Munmap(srcp, filesize);             //line:netp:servestatic:munmap
    }
}

//11.9使用malloc\rio_readn\rio_writen复制内容
void serve_static_malloc(int fd, char *filename, int filesize){
    int srcfd;
    char *srcp, filetype[MAXLINE], buf[MAXBUF];
    void *file_malloc_ptr;

    /* Send response headers to client */
    get_filetype(filename, filetype);    //line:netp:servestatic:getfiletype
    sprintf(buf, "HTTP/1.0 200 OK\r\n"); //line:netp:servestatic:beginserve
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Server: Tiny Web Server\r\n");
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Content-length: %d\r\n", filesize);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Content-type: %s\r\n\r\n", filetype);
    rio_writen(fd, buf, strlen(buf));    //line:netp:servestatic:endserve

    /* Send response body to client */
    srcfd = Open(filename, O_RDONLY, 0); //line:netp:servestatic:open

    // srcp = Mmap(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0); //line:netp:servestatic:mmap
    file_malloc_ptr=malloc(filesize);
    Rio_readn(srcfd, file_malloc_ptr, filesize);
    Close(srcfd);                       //line:netp:servestatic:close
    // rio_writen(fd, srcp, filesize);     //line:netp:servestatic:write
    rio_writen(fd, file_malloc_ptr, filesize); 
    // Munmap(srcp, filesize);             //line:netp:servestatic:munmap
    free(file_malloc_ptr);
}

/*
 * get_filetype - derive file type from file name
 */
void get_filetype(char *filename, char *filetype) 
{
    if (strstr(filename, ".html"))
	strcpy(filetype, "text/html");
    else if (strstr(filename, ".gif"))
	strcpy(filetype, "image/gif");
    else if (strstr(filename, ".png"))
	strcpy(filetype, "image/png");
    else if (strstr(filename, ".jpg"))
	strcpy(filetype, "image/jpeg");
    //11.7对mpg视频文件的扩展
    else if (strstr(filename, ".mpg"))
	strcpy(filetype, "video/mpeg");
    else
	strcpy(filetype, "text/plain");
}  
/* $end serve_static */

/*
 * serve_dynamic - run a CGI program on behalf of the client
 */
/* $begin serve_dynamic */
void serve_dynamic(int fd, char *filename, char *cgiargs) 
{
    char buf[MAXLINE], *emptylist[] = { NULL };

    /* Return first part of HTTP response */
    sprintf(buf, "HTTP/1.0 200 OK\r\n"); 
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Server: Tiny Web Server\r\n");
    rio_writen(fd, buf, strlen(buf));
  
    if (Fork() == 0) { /* Child */ //line:netp:servedynamic:fork
        /* Real server would set all CGI vars here */
        //11.11 HEAD方法不输出body 设置环境变量
        setenv("IS_HEAD", is_head?"1":"0", 1);
        //11.12 POST方法的参数在body中
        setenv("QUERY_STRING", cgiargs, 1); //line:netp:servedynamic:setenv
        Dup2(fd, STDOUT_FILENO);         /* Redirect stdout to client */ //line:netp:servedynamic:dup2
        Execve(filename, emptylist, environ); /* Run CGI program */ //line:netp:servedynamic:execve
    }
    // 11.8设置信号处理后，将原等待注释
    // Wait(NULL); /* Parent waits for and reaps child */ //line:netp:servedynamic:wait
}
/* $end serve_dynamic */

/*
 * clienterror - returns an error message to the client
 */
/* $begin clienterror */
void clienterror(int fd, char *cause, char *errnum, 
		 char *shortmsg, char *longmsg) 
{
    char buf[MAXLINE];

    /* Print the HTTP response headers */
    sprintf(buf, "HTTP/1.0 %s %s\r\n", errnum, shortmsg);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "Content-type: text/html\r\n\r\n");
    rio_writen(fd, buf, strlen(buf));

    /* Print the HTTP response body */
    sprintf(buf, "<html><title>Tiny Error</title>");
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<body bgcolor=""ffffff"">\r\n");
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "%s: %s\r\n", errnum, shortmsg);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<p>%s: %s\r\n", longmsg, cause);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<hr><em>The Tiny Web server</em>\r\n");
    rio_writen(fd, buf, strlen(buf));
}
/* $end clienterror */

//11.8 子进程信号处理 信号处理函数
void sigchld_handler(int sig){

    int olderrno = errno;

    sigset_t mask_all, prev_all;
    pid_t pid;
    int status;
    char *status_str;

    Sigfillset(&mask_all);
    Sigprocmask(SIG_BLOCK, &mask_all, &prev_all);

    while((pid = waitpid(-1, &status, WNOHANG|WUNTRACED)) > 0){
        if(WIFSTOPPED(status)){
            printf("[%d] %s by signal %d\n",
                pid, strsignal(WSTOPSIG(status)), WSTOPSIG(status));
        }else if(WIFSIGNALED(status)){
            printf("[%d] %s by signal %d\n",
                pid, strsignal(WTERMSIG(status)), WTERMSIG(status));            
        }
    }

    Sigprocmask(SIG_SETMASK, &prev_all, NULL);

    errno = olderrno;;

    return;
}

//11.12 POST方法，读取body的参数，保存到buf中
void read_requesthdrs_post(rio_t *rp, char *buf) 
{
    int content_length=0;

    Rio_readlineb(rp, buf, MAXLINE);
    printf("%s", buf);
    while(strcmp(buf, "\r\n")) {          //line:netp:readhdrs:checkterm
        Rio_readlineb(rp, buf, MAXLINE);
        printf("%s", buf);
        //11.12读取报头中Content-Length的信息得到body长度
        if(strstr(buf,"Content-Length:")!=NULL){
            sscanf(buf+15, "%d", &content_length);
        }
    } 
    //Rio_readlineb为安全函数，长度为有效长度+1 最后为 '\0'
    //注意Rio_readlineb与Rio_readn的区别为有无缓冲
    //如果在使用有缓冲的函数后再调用无缓冲的，无缓冲函数读不到已被缓冲的内容
    // Rio_readlineb(rp, buf, content_length+1);
    // 使用rio_readnb更妥当，但也要注意，rio_readnb的长度为有效长度
    rio_readnb(rp, buf, content_length);
    buf[content_length]='\0';
    printf("%s\n", buf);

    return;
}

//11.13 SIGPIPE信号处理
void sigpipe_handler(int sig){

    sigset_t mask_all, prev_all;
    pid_t pid;
    int status;
    char *status_str;

    Sigfillset(&mask_all);
    Sigprocmask(SIG_BLOCK, &mask_all, &prev_all);

    printf("%s\n",strerror(errno));

    Sigprocmask(SIG_SETMASK, &prev_all, NULL);

    return;    
}
