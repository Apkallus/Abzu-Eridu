/* $begin shellmain */
#include "csapp.h"
#define MAXARGS 128
#define JOBSNUM 7

/*
    链接
gcc -o res res.c csapp.c
    不完全版本
    关联 tshlab
*/ 

/* Function prototypes */
void eval(char *cmdline);
int parseline(char *buf, char **argv);
int builtin_command(char **argv); 

//jobs
//数组下标0弃用
volatile sig_atomic_t fgjob=0;
pid_t jobstab[JOBSNUM];
//初始化job列表
void initjobs(void){
    memset(jobstab,0,sizeof(jobstab));
}
//添加到job列表
int addjob(pid_t pid){
    int i;
    for(i=1;i<JOBSNUM;i++){
        if(jobstab[i]==0){
            jobstab[i]=pid;
            sio_putl(i);
            sio_puts(" ");
            sio_putl(jobstab[i]);
            sio_puts("\n");
            break;
        }
    }
    return i;
}
//从job列表中删除
void deletejob(pid_t pid){
    if(pid){
        for(int i=1;i<JOBSNUM;i++){
            if(jobstab[i]==pid){
                jobstab[i]=0;
                break;
            }
        }
    }

}

//使用 /proc/[PID]/stat 文件读取进程状态信息
//使用 /proc/[PID]/cmdline 文件读取进程命令
char *state_cts(char state);
void jobsinfo(void){
    for(int i=1;i<JOBSNUM;i++){
        pid_t pid=jobstab[i];
        if(pid!=0){
            char path[128], cmdline[128],state;
            int size,tpgid;
            FILE *fp;

            //使用 /proc/[PID]/stat 文件读取进程状态信息
            snprintf(path,sizeof(path),"/proc/%d/stat",pid);   
            fp=Fopen(path,"r");
            // %*d 表示忽略此int 
            // 文件使用空格分隔 能够读取系统前台进程id
            fscanf(fp,"%*d %*s %c %*d %*d %*d %*d %d",
                &state,&tpgid);
            Fclose(fp);
            if(pid==tpgid){
                //如果为系统前台进程则跳过
                continue;
            }
            printf("[%d] %d %c %s\t",i,pid,state,state_cts(state));

            //使用 /proc/[PID]/cmdline 文件读取进程命令
            snprintf(path,sizeof(path),"/proc/%d/cmdline",pid);
            fp=Fopen(path,"r");
            size=Fread(cmdline,1,128,fp);
            Fclose(fp);

            int k;
            for(k=0;k<size;k++){
                // 文件使用'\0'分隔
                if(cmdline[k]=='\0'){
                    cmdline[k]=' ';
                }
            }
            cmdline[k]='\0';
            //前面已经排除了前台进程，直接输出&符号
            printf("%s &\n",cmdline);
        }
    }
}
//状态字符对应字符串
char *state_cts(char state){
    char *res=NULL;
    switch(state){
        case 'R':
            res="running";
            break;
        case 'S':
            res="sleeping";
            break;
        case 'D':
            res="waiting";
            break;
        case 'Z':
            res="zombie";
            break;
        case 'T':
            res="stopped";
            break;
        case 'W':
            res="paging";
            break;
    }
    return res;
}

// 信号处理程序
int pre_bgorfg(pid_t pid){
    int tpgid, isbg=1; 
    tpgid=tcgetpgrp(0);
    printf("shell id=%d,pid=%d,tpgit=%d",getpid(),pid,tpgid);
    //自定义shell为系统前台进程，应当在此保存shell的前台信息
    if(pid==tpgid){
        //tpgid控制终端的前台进程组id
        isbg=0;
    }
    return isbg;
}

int bgorfg(pid_t pid){
    return pid==fgjob;
}

void absig(pid_t pid,int status){
    if(WIFSIGNALED(status)){
        sio_putl(pid);
        sio_puts(" ");
        sio_puts(strsignal(WTERMSIG(status)));
        sio_puts("\n");
    }else if(WIFSTOPPED(status)){
        sio_putl(pid);
        sio_puts(" ");
        sio_puts(strsignal(WSTOPSIG(status)));
        sio_puts("\n");        
    }
}
// Ctrl+C 信号处理程序
void sig_int_handler(int sig){
    int olderrno =errno;
    sigset_t mask_all, prev_all;

    Sigfillset(&mask_all);  
    Sigprocmask(SIG_BLOCK,&mask_all,&prev_all);    
    if(fgjob!=0){
        sio_puts("\nsig_int_handler ");
        sio_putl(-fgjob);
        sio_puts(" ");
        sio_putl(sig);
        sio_puts("\n");
        sio_putl(kill(fgjob,0));
        sio_puts("\n");

        kill(-fgjob,SIGINT);
        fgjob=0;
    }
    Sigprocmask(SIG_SETMASK,&prev_all,NULL);        
    errno=olderrno;
}
// Ctrl+Z 信号处理程序
void sig_tstp_handler(int sig){
    int olderrno =errno;
    sigset_t mask_all, prev_all;

    Sigfillset(&mask_all);  
    Sigprocmask(SIG_BLOCK,&mask_all,&prev_all);    
    if(fgjob!=0){
        sio_puts("\nsig_tstp_handler ");
        sio_putl(-fgjob);
        sio_puts(" ");
        sio_putl(sig);
        sio_puts("\n");
        sio_putl(kill(fgjob,0));
        sio_puts("\n");

        kill(-fgjob,SIGTSTP);
        fgjob=0;
    }
    Sigprocmask(SIG_SETMASK,&prev_all,NULL);        
    errno=olderrno;
}
// 子程序信号处理程序
void sigchld_handler(int sig){ 
    int olderrno =errno;
    sigset_t mask_all, prev_all;
    pid_t pid;
    int status;
    Sigfillset(&mask_all);
    
    // printf("into sigchld_handler\n");
    while ((pid=waitpid(-1, &status, WNOHANG|WUNTRACED)) > 0){
        Sigprocmask(SIG_BLOCK,&mask_all,&prev_all);
        sio_puts("\nsigchld_handler pid ");
        sio_putl(pid);
        sio_puts("\n");

        absig(pid,status);
        if (!(WIFSTOPPED(status))){
            deletejob(pid);
        }        
        if(fgjob==pid){
            fgjob=0;
        }
        Sigprocmask(SIG_SETMASK,&prev_all,NULL);        
    }
    // if(errno!=ECHILD){
    //     sio_error("waitpid error\n");
    // }
    errno=olderrno;
}

int main() 
{
    char cmdline[MAXLINE]; /* Command line */
    //初始化job
    initjobs();
    //安装信号处理程序，子程序之后要恢复默认
    Signal(SIGINT,sig_int_handler);
    Signal(SIGTSTP,sig_tstp_handler);

    while (1) {
        /* Read */
        printf("shell> ");                   
        Fgets(cmdline, MAXLINE, stdin); 
        if (feof(stdin))
            exit(0);

        /* Evaluate */
        eval(cmdline);
    } 
}

void fg(pid_t pid,sigset_t prev_one){
    sio_puts("void fg(pid_t pid,sigset_t prev_one)\n");
    sio_putl(pid);
    sio_puts(" ");
    sio_putl(fgjob);
    sio_puts("\n");
    while (fgjob){
        sio_puts("while (fgjob) ");
        sio_putl(fgjob);
        sio_puts("\n");
        sigsuspend(&prev_one);
    }     
}
void eval(char *cmdline) 
{
    char *argv[MAXARGS]; /* Argument list execve() */
    char buf[MAXLINE];   /* Holds modified command line */
    int bg, jobsindex;              /* Should the job run in bg or fg? */
    pid_t pid;           /* Process id */
    
    sigset_t mask_one, prev_one;
    Sigemptyset(&mask_one);
    Sigaddset(&mask_one,SIGCHLD);
    Signal(SIGCHLD,sigchld_handler);

    strcpy(buf, cmdline);
    bg = parseline(buf, argv); 
    if (argv[0] == NULL)  
	    return;   /* Ignore empty lines */

    if (!builtin_command(argv)) { 
        Sigprocmask(SIG_BLOCK,&mask_one,&prev_one);
        if ((pid = Fork()) == 0) {   /* Child runs user job */
            // //在子程序中恢复信号处理程序到默认
            Signal(SIGINT,SIG_DFL);
            Signal(SIGTSTP,SIG_DFL);
            Signal(SIGCHLD, SIG_DFL);
            // 在子进程中设置子进程的pgid为子进程pid    
            setpgid(0,0);   
            Sigprocmask(SIG_SETMASK,&prev_one,NULL);
            Execve(argv[0], argv, environ);
        }

        //&mask_all,&prev_one将prev_one设置为阻止接受子程序信号，导致后台全部为僵尸
        /* Parent waits for foreground job to terminate */
        // 在父进程中同步设置子进程的pgid
        setpgid(pid,pid);
        // 在父进程中调用addjob
        jobsindex=addjob(pid);
        // tcsetpgrp(STDIN_FILENO,pid);
        if (!bg){
            sio_puts("if (!bg)\n");
            fgjob=pid;
        }
        
        if (bgorfg(pid)){
            sio_puts("if (bgorfg(pid))\n");
            fg(pid,prev_one);
        }else{
            sio_puts("else\n");
            printf("[%d] %d %s\n",jobsindex, pid, cmdline);
        }
        Sigprocmask(SIG_SETMASK,&prev_one,NULL);

    }
    return;
}

int builtin_command(char **argv) 
{
    if (!strcmp(argv[0], "quit")) /* quit command */
	    exit(0);  
    if (!strcmp(argv[0], "&"))    /* Ignore singleton & */
	    return 1;
    if (!strcmp(argv[0], "jobs")){
        // printf("into builtin_command jobs\n");
        jobsinfo();
        return 1;
    }

    if (!strcmp(argv[0], "bg")||!strcmp(argv[0], "fg")){
        sigset_t mask_one, prev_one;
        Sigemptyset(&mask_one);
        Sigaddset(&mask_one,SIGCHLD);
        Sigprocmask(SIG_BLOCK,&mask_one,&prev_one);
        char *argv1=argv[1];
        pid_t pid;
        if(argv1[0]=='%'){
            //如果是jid 指针后移
            argv1++;
            pid=jobstab[atoi(argv1)];
            sio_puts(argv1);
            sio_puts("\t");
            sio_putl(atoi(argv1));
            sio_puts("\t");
        }else{
            pid=atoi(argv1);
        }
        sio_putl(pid);
        sio_puts("\t bg fg \n");
        if (!strcmp(argv[0], "bg")){
            Kill(-pid, SIGCONT);    
            if(bgorfg(pid)){
                fgjob=0;
            }       
        }
        if (!strcmp(argv[0], "fg")){
            Kill(-pid, SIGCONT);
            if(!bgorfg(pid)){
                fgjob=pid;
                fg(pid,prev_one);
            }
        }
        Sigprocmask(SIG_SETMASK,&prev_one,NULL);
        return 1;
    }
    return 0;                     /* Not a builtin command */
}

int parseline(char *buf, char **argv) 
{
    char *delim;         /* Points to first space delimiter */
    int argc;            /* Number of args */
    int bg;              /* Background job? */

    buf[strlen(buf)-1] = ' ';  /* Replace trailing '\n' with space */
    while (*buf && (*buf == ' ')) /* Ignore leading spaces */
	buf++;

    /* Build the argv list */
    argc = 0;
    while ((delim = strchr(buf, ' '))) {
	argv[argc++] = buf;
	*delim = '\0';
	buf = delim + 1;
	while (*buf && (*buf == ' ')) /* Ignore spaces */
            buf++;
    }
    argv[argc] = NULL;
    
    if (argc == 0)  /* Ignore blank line */
	return 1;

    /* Should the job run in the background? */
    if ((bg = (*argv[argc-1] == '&')) != 0)
	argv[--argc] = NULL;

    return bg;
}