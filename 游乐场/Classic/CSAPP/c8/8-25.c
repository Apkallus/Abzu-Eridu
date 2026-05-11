#include "csapp.h"

jmp_buf tfgets_buf;
void sigit_handler(int sig){
    printf("%s\n",strsignal(sig));
    longjmp(tfgets_buf, 1);
}
char *tfgets(char *str, int n, FILE *stream){
    char *res=NULL;
    //设置闹钟信号的信号处理函数
    if(signal(SIGALRM, sigit_handler) == SIG_ERR){
        printf("signal error");
    }
    //设置5秒的闹钟信号
    alarm(5);
    //使用setjmp保存调用环境
    if(!setjmp(tfgets_buf)){
        //设置环境时进入此分支调用fgets
        //如在收到闹钟信号前得到输入则继续返回指针
        res = fgets(str, n, stream);
    }else{
        //收到闹钟信号后跳过fgets返回res为NULL
    }
    return res;
}
int main(void){

    char buf[128];
    if(tfgets(buf, sizeof(buf), stdin)!=NULL){
        puts(buf);
    }

    return 0;
}