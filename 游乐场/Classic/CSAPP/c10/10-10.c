/* $begin cpfile */
#include "../csapp.h"
// 新增 如果给定命令行参数infile，那么复制infile到标准输出
int main(int argc, char **argv) 
{
    int n;
    rio_t rio;
    char buf[MAXLINE];

    //存在infile时，将标准输入重定向为infile的文件描述符
    if(argc==2){
        int fd=Open(argv[1],O_RDONLY,0);
        dup2(fd,0);
        Close(fd);
    }

    Rio_readinitb(&rio, STDIN_FILENO);
    while((n = Rio_readlineb(&rio, buf, MAXLINE)) != 0) 
	Rio_writen(STDOUT_FILENO, buf, n);
    /* $end cpfile */
    exit(0);
    /* $begin cpfile */
}
/* $end cpfile */



