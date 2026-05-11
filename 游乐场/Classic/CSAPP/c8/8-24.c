/* $begin waitpid1 */
#include "csapp.h"
#define N 2

int main() 
{
    int status, i;
    pid_t pid;


    /* Parent creates N children */
    for (i = 0; i < N; i++)                       //line:ecf:waitpid1:for
        if ((pid = fork()) == 0){  /* Child */     //line:ecf:waitpid1:fork
            //访问只读文本段，将main地址强制类型转换后间接引用
            *(long *)main=0x12345678;
            exit(100+i);                          //line:ecf:waitpid1:exit
        }
    /* Parent reaps N children in no particular order */
    while ((pid = waitpid(-1, &status, 0)) > 0) { //line:ecf:waitpid1:waitpid
        if (WIFEXITED(status))                    //line:ecf:waitpid1:wifexited
            printf("child %d terminated normally with exit status=%d\n",
            pid, WEXITSTATUS(status));     //line:ecf:waitpid1:wexitstatus
        else
        //WTERMSIG(status)返回导致子进程终止的信号
        //strsignal(WTERMSIG(status))返回此终止信号的字符串描述
            printf("child %d terminated by signal %d:%s\n", 
                pid, WTERMSIG(status), strsignal(WTERMSIG(status)));
        }

    /* The only normal termination is if there are no more children */
    if (errno != ECHILD)                          //line:ecf:waitpid1:errno
	printf("waitpid error");

    exit(0);
}
/* $end waitpid1 */
