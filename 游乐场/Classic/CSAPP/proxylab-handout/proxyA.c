#include <stdio.h>
#include "csapp.h"

/* Recommended max cache and object sizes */
#define MAX_CACHE_SIZE 1049000
#define MAX_OBJECT_SIZE 102400

/* You won't lose style points for including this long line in your code */
static const char *user_agent_hdr = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3\r\n";

void doit(int fd);
void read_client_requesthdrs(rio_t *rp, char *client_requesthdrs_buf,
    char *server_ip, char *server_port);
void clienterror(int fd, char *cause, char *errnum, 
		 char *shortmsg, char *longmsg);
void send_to_server(int proxy_as_clientfd, char *client_requesthdrs_buf);
void *read_server_requesthdrs(rio_t *server_rio, 
    char *server_requesthdrs_buf, int *file_size);
void send_to_client(int client_fd , char *server_requesthdrs_buf, 
        char *server_body_ptr, int file_size);
void sigpipe_handler(int sig);


int main(int argc, char *argv[])
{
    int listenfd, connfd;
    char hostname[MAXLINE], port[MAXLINE];
    socklen_t clientlen;
    struct sockaddr_storage clientaddr;

    //无论阻塞pipe信号后，创建包装写入函数关闭连接描述符来防止终止
    //还是创建信号处理程序，每次写入时都进行检测
    //都不妥当，当前按照信号处理程序处理
    Signal(SIGPIPE, sigpipe_handler);

    /* Check command line args */
    if (argc != 2) {
        fprintf(stderr, "usage: %s <port>\n", argv[0]);
        exit(1);
    }

    //作为服务器打开监听端口，读取目标客户端请求
    listenfd = Open_listenfd(argv[1]);
    while(1){
        clientlen = sizeof(clientaddr);
        connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen);
        Getnameinfo((SA *)&clientaddr, clientlen, hostname, MAXLINE,
            port, MAXLINE, 0);
        printf("Accepted connection from (%s, %s)\n", hostname, port);
        doit(connfd);
        Close(connfd);
        printf("---end of main loop---\n");
    }

    return 0;
}

void doit(int fd){
    rio_t rio, server_rio;
    char buf[MAXLINE], client_requesthdrs_buf[MAXLINE];
    char method[MAXLINE], uri[MAXLINE], version[MAXLINE];
    char server_ip[MAXLINE], server_port[MAXLINE];
    int proxy_as_clientfd;
    char *server_body_ptr, server_requesthdrs_buf[MAXLINE];
    char *tp, *urip, tbuf[MAXLINE];
    int file_size = 0;

    server_ip[0]='\0';
    server_port[0]='\0';

    //初始化健壮包并读取客户端请求头
    Rio_readinitb(&rio, fd);
    if(!Rio_readlineb(&rio, buf, MAXLINE)){
        return;
    }
    printf("orgin >> Request headers:\n%s",buf);
    sscanf(buf, "%s %s %s", method, uri, version);
    //将客户端请求头始终转为HTTP/1.0发送
    //并且从URL中拆分URI
    urip = uri;
    if(strstr(uri, "http")){
        // http://localhost:1234/home.html
        tp = strstr(uri, "://") + 3;
        //urip指向URI开头的 '/'
        urip = strchr(tp, '/');
        printf("urip = strchr(tp, '/')  >%s<\n",urip);
        //拆分并得到ip与port
        strcpy(tbuf, tp);
        tp = strchr(tbuf, '/');
        *tp = '\0';

        if((tp = strchr(tbuf, ':'))){
            //如果包括端口
            *tp = '\0';
            strcpy(server_port, tp+1);
        }
        strcpy(server_ip, tbuf);
    } 
    printf("urip = strchr(tp, '/')  >%s<\n",urip);
    sprintf(client_requesthdrs_buf
        ,"%s %s %s\r\n", method, urip, "HTTP/1.0");
    printf("%s",client_requesthdrs_buf);

    //如果请求方法不是GET则返回
    if (strcasecmp(method, "GET")) {
        clienterror(fd, method, "501", "Not Implemented",
                    "Proxy does not implement this method");
        return;
    }  
    
    // 继续读取并处理请求头,同时得到服务器ip与port
    read_client_requesthdrs(&rio, client_requesthdrs_buf,
            server_ip, server_port); 

    // 将处理后的客户端的请求头，转发到服务器
    // 服务器的ip与port来源于客户端的host头
    // 由read_client_requesthdrs函数获得
    proxy_as_clientfd = Open_clientfd(server_ip, 
            server_port[0]=='\0'?NULL:server_port);
    Rio_readinitb(&server_rio, proxy_as_clientfd);

    send_to_server(proxy_as_clientfd, client_requesthdrs_buf);

    server_body_ptr = read_server_requesthdrs(&server_rio, 
        server_requesthdrs_buf, &file_size);
    
    send_to_client(rio.rio_fd ,server_requesthdrs_buf, 
        server_body_ptr, file_size);
    
}

// 读取并处理客户端请求头
void read_client_requesthdrs(rio_t *rp, char *client_requesthdrs_buf,
    char *server_ip, char *server_port){
    char buf_temp[MAXLINE], *tp, server_buf[MAXLINE];
    char *close_header = "close\r\n";
    do {          
        Rio_readlineb(rp, buf_temp, MAXLINE);
        //更改客户端的两个连接到close
        if(strstr(buf_temp, "Connection:") == buf_temp
        ||strstr(buf_temp, "Proxy-Connection:") == buf_temp){
            printf("orgin >> %s", buf_temp);
            tp = strchr(buf_temp, ':') + 2;
            strcpy(tp, close_header);

        }else if(strstr(buf_temp, "User-Agent:")){
            printf("orgin >>%s", buf_temp);
            strcpy(buf_temp, user_agent_hdr);

        }else if(strstr(buf_temp, "Host:")){
            printf("1. buf_temp=%s",buf_temp);
            tp = strchr(buf_temp, ':') + 2;
            strcpy(server_buf, tp);
            //在冒号与空格后，server_buf保存host头的值：ip与可能的port
            tp = strchr(server_buf, '\r');
            *tp = '\0';
            if((tp = strchr(server_buf, ':'))){
                //如果host中有port内容
                *tp = '\0';
                strcpy(server_port, tp+1);
            }
            strcpy(server_ip, server_buf);
            
            printf("server_ip=>>%s<< server_port=>>%s<<\n",
            server_ip, server_port);
        }
        strcat(client_requesthdrs_buf, buf_temp);
        printf("%s", buf_temp);
    } while((strcmp(buf_temp, "\r\n")));
    //报头后的空行判断其是否结束
    printf("----out read_requesthdrs----\n");
    return;   
}

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
    sprintf(buf, "<html><title>proxy Error</title>");
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<body bgcolor=""ffffff"">\r\n");
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "%s: %s\r\n", errnum, shortmsg);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<p>%s: %s\r\n", longmsg, cause);
    rio_writen(fd, buf, strlen(buf));
    sprintf(buf, "<hr><em>The proxy Web server</em>\r\n");
    rio_writen(fd, buf, strlen(buf));
}
/* $end clienterror */

void send_to_server(int proxy_as_clientfd, char *client_requesthdrs_buf){
    printf("----into send_to_server----\n");

    printf("%s",client_requesthdrs_buf);
    //将客户端内容转发到服务器
    Rio_writen(proxy_as_clientfd, client_requesthdrs_buf, 
        strlen(client_requesthdrs_buf));

    printf("----out send_to_server----\n");
}

//读取服务器报头到buf
void *read_server_requesthdrs(rio_t *server_rio, 
    char *server_requesthdrs_buf, int *file_size){

    char buf[MAXLINE];
    void *server_malloc_ptr = NULL;

    Rio_readlineb(server_rio, server_requesthdrs_buf, MAXLINE);    
    printf("%s",server_requesthdrs_buf);
    while((strcmp(buf, "\r\n"))) {
        Rio_readlineb(server_rio, buf, MAXLINE);
        strcat(server_requesthdrs_buf, buf);
        printf("%s",buf);
        if(strstr(buf, "Content-length:")){
            sscanf(buf, "Content-length: %d", file_size);
            printf("file_size = %d\n",*file_size);
        }
    }
    if(*file_size){
        server_malloc_ptr = malloc(*file_size);
        Rio_readnb(server_rio, server_malloc_ptr, *file_size);
    }

    return server_malloc_ptr;   
}

void send_to_client(int client_fd , char *server_requesthdrs_buf, 
    char *server_body_ptr, int file_size){
    int check;
    printf("----into send_to_client----\n");

    //将客户端内容转发到服务器
    check = rio_writen(client_fd, server_requesthdrs_buf, 
        strlen(server_requesthdrs_buf));
    if(check==-1){
        if(server_body_ptr){
            free(server_body_ptr);
        }
        return;
    }

    if(server_body_ptr){
        check = rio_writen(client_fd, server_body_ptr, 
            file_size);  
        free(server_body_ptr);
        if(check==-1)return;
    }
    printf("----out send_to_client----\n");        
}

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
