#include <stdio.h>
#include "csapp.h"
#include "sbuf.h"

//B.
//线程数量
#define NTHREADS  4
//缓冲的连接描述符数量
#define SBUFSIZE  16
//缓冲区结构
sbuf_t sbuf; /* Shared buffer of connected descriptors */

struct cache {
    char file_url[MAXLINE];
    char type[MAXLINE];
    char *file_content;
    long length;
    long last;
    struct cache *next;
    struct cache *prev;
} *cache_link_ptr = NULL;

/* Recommended max cache and object sizes */
#define MAX_CACHE_SIZE 1049000
#define MAX_OBJECT_SIZE 102400

/* You won't lose style points for including this long line in your code */
static const char *user_agent_hdr = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3\r\n";


long int cache_last = 0;
long int cache_size = 0;

int readcnt;
sem_t mutex, w;

void doit(int fd);
void read_client_requesthdrs(rio_t *rp, char *client_requesthdrs_buf,
    char *server_ip, char *server_port);
void clienterror(int fd, char *cause, char *errnum, 
		 char *shortmsg, char *longmsg);
void send_to_server(int proxy_as_clientfd, char *client_requesthdrs_buf);
void *read_server_requesthdrs(rio_t *server_rio, 
    char *server_requesthdrs_buf, int *file_size,
    char *file_type);
void send_to_client(int client_fd , char *server_requesthdrs_buf, 
        char *server_body_ptr, int file_size);
void sigpipe_handler(int sig);
void *thread(void *vargp);
struct cache *is_exist(char *cache_file_url);
void add_to_cache(char *cache_file_url, int file_size
    , char *file_type, char *server_body_ptr);
void write_to_cache(char *cache_file_url, int file_size
    , char *file_type, int diff, char *server_body_ptr);
void expel_to_cache(int diff);
void delete_to_cache(struct cache *delete_ptr);
void send_cache_to_client(int fd, struct cache *file_ptr);
void lock_init();

int main(int argc, char *argv[])
{
    int listenfd, connfd;
    char hostname[MAXLINE], port[MAXLINE];
    socklen_t clientlen;
    struct sockaddr_storage clientaddr;
    pthread_t tid;
    
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

    sbuf_init(&sbuf, SBUFSIZE);
    //B.初始化连接描述符缓冲区
    for (int i = 0; i < NTHREADS; i++)  /* Create worker threads */ //line:conc:pre:begincreate
	    Pthread_create(&tid, NULL, thread, NULL);   
    //B.创造线程
    //初始化锁
    lock_init();

    while(1){
        clientlen = sizeof(clientaddr);
        connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen);
        //B.将连接描述符更新到缓冲区
        sbuf_insert(&sbuf, connfd);
        // Getnameinfo((SA *)&clientaddr, clientlen, hostname, MAXLINE,
        //     port, MAXLINE, 0);
        // printf("Mainthread accepted connection from (%s, %s)\n", hostname, port);
        //B.主线程监听，创建的线程处理
        // doit(connfd);
        //B.将关闭连接描述符转移到工作线程中
        // Close(connfd);
        // printf("---end of main loop---\n");
    }

    return 0;
}

void *thread(void *vargp) 
{  
    pthread_t tid = pthread_self();
    Pthread_detach(tid); 
    //分离线程以在结束后回收内存资源
    printf("creat pthread[%u]\n",tid);
    while (1) { 
        int connfd = sbuf_remove(&sbuf); /* Remove connfd from buffer */ //line:conc:pre:removeconnfd
        //从池中获得连接描述符
        printf("pthread[%u] accepted connection\n",tid);
        doit(connfd);                /* Service client */
        //调用处理函数
        Close(connfd);
        printf("pthread[%u] closed connection\n",tid);
    }
}
void doit(int fd){
    rio_t rio, server_rio;
    char buf[MAXLINE], client_requesthdrs_buf[MAXLINE];
    char method[MAXLINE], uri[MAXLINE], version[MAXLINE];
    char server_ip[MAXLINE], server_port[MAXLINE];
    int proxy_as_clientfd;
    char *server_body_ptr = NULL, server_requesthdrs_buf[MAXLINE];
    char *tp, *urip, tbuf[MAXLINE];
    int file_size = 0;
    char cache_file_url[MAXLINE];
    struct cache *cache_file_ptr;
    char file_type[MAXLINE];

    server_ip[0]='\0';
    server_port[0]='\0';

    // static pthread_once_t once =PTHREAD_ONCE_INIT;
    // pthread_once(&once, NULL);
    // //线程初始化

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

    // C.得到文件URL
    sprintf(cache_file_url, "%s:%s%s",
        server_ip,server_port,urip);
    printf("-->>>cache_file_url>%s<\n",
        cache_file_url);   


    // 搜索此URL是否被代理缓存
    cache_file_ptr = is_exist(cache_file_url);
    // 如果代理缓存则发送到客户端并返回
    if(cache_file_ptr){
        printf("-->>>cproxy have the file\n");
        //  C.读者
        P(&mutex);
        readcnt++;
        if(readcnt == 1)
            P(&w);
        V(&mutex);

        if(is_exist(cache_file_url))
            send_cache_to_client(fd, cache_file_ptr);

        P(&mutex);
        readcnt--;
        if(readcnt == 0)
            V(&w);
        V(&mutex);        
        return;
    }
    

    // 否则向服务器转发
    printf("-->>>cproxy do not have the file\n");
    

    // 将处理后的客户端的请求头，转发到服务器
    // 服务器的ip与port来源于客户端的host头
    // 由read_client_requesthdrs函数获得
    proxy_as_clientfd = Open_clientfd(server_ip, 
            server_port[0]=='\0'?NULL:server_port);
    Rio_readinitb(&server_rio, proxy_as_clientfd);

    send_to_server(proxy_as_clientfd, client_requesthdrs_buf);

    server_body_ptr = read_server_requesthdrs(&server_rio, 
        server_requesthdrs_buf, &file_size, file_type);
    
    send_to_client(rio.rio_fd ,server_requesthdrs_buf, 
        server_body_ptr, file_size);
    
    P(&w);
    //  C.写者
    if(!is_exist(cache_file_url))
        add_to_cache(cache_file_url, file_size, file_type, server_body_ptr);
    V(&w);

    printf("======= enf of doit ==========\n");
    if(server_body_ptr)
        free(server_body_ptr);
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
    char *server_requesthdrs_buf, int *file_size,
    char *file_type){

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
        //C.再得到文件类型
        if(strstr(buf, "Content-type:")){
            strcpy(file_type, buf);
            printf("file_type = %s\n",file_type);
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
            // free(server_body_ptr);
        }
        return;
    }

    if(server_body_ptr){
        check = rio_writen(client_fd, server_body_ptr, 
            file_size);  
        // free(server_body_ptr);
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

struct cache *is_exist(char *cache_file_url){
    struct cache *find = NULL, *index_ptr;
    for(index_ptr = cache_link_ptr; index_ptr; 
        index_ptr = index_ptr->next){
        if(strcmp(index_ptr->file_url, cache_file_url) == 0){
            find = index_ptr;
            printf("find!\n");
            break;
        }
    }
    return find;
}

void add_to_cache(char *cache_file_url, int file_size
    , char *file_type ,char *server_body_ptr){
    printf("======= into add_to_cache ==========\n");  
    if(file_size > MAX_OBJECT_SIZE){
        //如果文件大小超出最大缓存对象上限则返回
        return;
    }

    //否则代理缓存此文件
    //diff = 最大缓存-当前缓存-文件大小
    int diff = MAX_CACHE_SIZE - cache_size - file_size;
    printf("=== diff = %d===\n", diff);
    if(diff < 0){
        
        //如果超过代理缓存上限则驱逐
        expel_to_cache(diff);
    }
    //直接写入或驱逐后写入
    write_to_cache(cache_file_url, file_size, file_type, 
        diff, server_body_ptr);

}

void write_to_cache(char *cache_file_url, int file_size
    , char *file_type, int diff, char *server_body_ptr){
    printf("======= into write_to_cache ==========\n");
    struct cache *file;
    file = (struct cache *)malloc(sizeof(struct cache));
    //创建并写入结构
    file->last = 0;
    strcpy(file->file_url, cache_file_url);
    file->length = file_size;
    strcpy(file->type, file_type);
    file->prev = NULL;
    file->next = cache_link_ptr;
    file->file_content = (char *)malloc(file_size);
    memcpy(file->file_content, server_body_ptr, file_size);
    if(file->next){
        file->next->prev = file;
    }
    cache_link_ptr = file;

    //更新缓存全局变量
    cache_size += file_size;
}

void expel_to_cache(int diff){
    printf("======= into expel_to_cache ==========\n");    
    diff = -diff;
    int expel_size = 0;
    struct cache *expel_ptr, *index_ptr;

    while(diff > expel_size){    
        //只要驱逐后得到的空间不足，就持续驱逐
        int i = 0;
        for(index_ptr = cache_link_ptr; index_ptr; 
            index_ptr = index_ptr->next){
            if(i==0){
                i = 1;
                expel_ptr = index_ptr;
            }else if(index_ptr->last < expel_ptr->last){
                //last越小越不常用，驱逐最小last
                expel_ptr = index_ptr;     
            }
        }
        expel_size += expel_ptr->length;
        delete_to_cache(expel_ptr);
    }
}

void delete_to_cache(struct cache *delete_ptr){
    printf("======= into delete_to_cache ==========\n");   
    //从链表中移除
    if(delete_ptr->prev)
        delete_ptr->prev->next = delete_ptr->next;
    

    if(delete_ptr->next){
        delete_ptr->next->prev = delete_ptr->prev;
    }
    //更新缓存全局变量并释放内存
    cache_size -= delete_ptr->length;
    free(delete_ptr->file_content);
    free(delete_ptr);
}

void send_cache_to_client(int fd, struct cache *file_ptr){
    char buf[MAXBUF],head_buf[MAXBUF];
    printf("======= into send_cache_to_client ==========\n");   
    
    P(&mutex);
    file_ptr->last++;
    V(&mutex);
    
    sprintf(head_buf, "HTTP/1.0 200 OK\r\n"); //line:netp:servestatic:beginserve
    strcat(head_buf, "Server: Proxy Web Server\r\n");
    sprintf(buf, "Content-length: %d\r\n", file_ptr->length);
    strcat(head_buf, buf);
    strcat(head_buf, file_ptr->type);
    strcat(head_buf, "\r\n");//报头空行
    rio_writen(fd, head_buf, strlen(head_buf));
    printf(">>%s<<",head_buf);
    printf("cache_size = %d \n",cache_size);

    rio_writen(fd, file_ptr->file_content, file_ptr->length);
}

void lock_init(){
    readcnt = 0;
    sem_init(&mutex, 0, 1);
    sem_init(&w, 0, 1);
}