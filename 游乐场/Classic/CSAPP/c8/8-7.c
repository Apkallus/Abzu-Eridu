#include <stdio.h>
#include <stdlib.h>
#include "csapp.h"

unsigned int snooze(unsigned int secs);

void sigit_handler(int sig){
    return ;//@ 休眠进程收到未被忽略的信号，sleep函数就提前返回
            //  将SIGINT信号的终止进程功能取消掉，控制回到sleep函数时将立即返回
}
int main(int argc, char *argv[]){

    //@判断参数数量
    if(argc!=2){
        fprintf(stderr, "usage: %s<secs>\n", argv[0]);
        exit(0);
    }
    //@将信号处理程序放在调用前来设置
    if(signal(SIGINT, sigit_handler) == SIG_ERR){
        unix_error("signal error");
    }
    //@argv[1]是字符指针，此处应当传入字符串对应的值
    (void)snooze(atoi(argv[1]));
    

    // snooze(argv[1]);
    // if(signal(SIGINT, sigit_handler) == SIG_ERR){
    //     unix_error("signal error");
    // }

    return 0;
}