/* $begin tfgetsmain */
#include "csapp.h"
#include <sys/select.h>
#include <sys/time.h>
#include <unistd.h>

char *tfgets(char *s, int size, FILE *stream);
/* $end tfgetsmain */


char *tfgets(char *s, int size, FILE *stream){
    
    int ret;
    char *res;
    struct timeval timeout;
    fd_set read_fd;

    //设置select监听描述符集合
    FD_ZERO(&read_fd);
    FD_SET(0, &read_fd);

    //设置超时结构变量
    timeout.tv_sec = 2;
    timeout.tv_usec = 0;

    //根据select返回值执行分支
    //select返回>0则为描述符，=0则为超时，<0则为异常
    if((ret = select(1, &read_fd, NULL, NULL, &timeout)) > 0){
        res = fgets(s, size, stream);  
    }else{
        res = NULL;
    }    

    return res;
}

int main() 
{
    char buf[MAXLINE];

    if (tfgets(buf, MAXLINE, stdin) == NULL)
	    printf("BOOM!\n");
    else 
	    printf("%s", buf);

    exit(0);
}