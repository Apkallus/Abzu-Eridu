/* $begin tfgetsmain */
#include "csapp.h"
#include <sys/time.h>
#include <setjmp.h>


char *tfgets(char *s, int size, FILE *stream);
void sigchld_handler(int sig);
void sigalrm_handler(int sig);
void sigusr1_handler(int sig);
/* $end tfgetsmain */

sigjmp_buf buf;

// 使用进程/信号/非本地跳转 不应使用alarm
// 非本地跳转为setjmp longjmp
// 子进程设置定时5秒信号与exit
// 主进程使用setjmp分支，调用fgets函数
// 若在收到子进程信号前从标准输入获得数据，则主进程kill发送终止信号到子进程
// 若收到，则使用信号处理函数longjum到setjmp分支返回NULL
char *tfgets(char *s, int size, FILE *stream){
    
    char *res;
    struct itimerval timer;
    pid_t time_pid, t_pid;

    sigset_t mask, prev;
    Signal(SIGCHLD, sigchld_handler);
    Signal(SIGUSR1, sigchld_handler);
    Sigemptyset(&mask);
    Sigaddset(&mask, SIGCHLD);
    t_pid = getpid();

    Sigprocmask(SIG_BLOCK, &mask, &prev);
    if((time_pid = fork()) == 0){
        //子进程设置定时与定时信号处理
        // Signal(SIGALRM, sigalrm_handler);
        // timer.it_value = (struct timeval){2, 0};
        // setitimer(ITIMER_REAL, &timer, NULL);
        //等待定时 以及主进程的终止信号

        //尝试用sigusr1_handler但无法收到信号，改用子进程终止作为信号
        sleep(2);
        // kill(t_pid, SIGUSR1);
        exit(0);
    }

    if(!sigsetjmp(buf, 1)){
        //主进程等待标准输入的数据，如获得则向子进程发送终止信号
        res = fgets(s, size, stream);  
        kill(time_pid ,SIGINT);     
    }else{
        //收到子进程终止信号则返回NULL
        res = NULL;
    }    

    Sigprocmask(SIG_SETMASK, &prev, NULL);
    return res;
}

//子进程定时信号处理函数
// void sigalrm_handler(int sig){
//     //向主进程发送SIGUSR1信号
//     kill(getppid(), SIGUSR1);
// }
//主进程接受子进程信号的处理函数
// void sigusr1_handler(int sig){
//     printf("sigusr1_handler\n");
//     //非本地跳转到条件判断
//     siglongjmp(buf, 1);
// }

void sigchld_handler(int sig){
    printf("sigchld_handler\n");
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

    //尝试用sigusr1_handler但无法收到信号，改用子进程终止作为信号
    siglongjmp(buf, 1);
    return;
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