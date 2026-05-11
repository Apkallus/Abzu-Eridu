/* 
 * hellobug.c - "hello, world" program with a bug
 */
/* $begin hellobug */
/* WARNING: This code is buggy! */
#include "csapp.h"
void *thread(void *vargp);

int main() 
{
    pthread_t tid;

    Pthread_create(&tid, NULL, thread, NULL);
    //A. 线程函数sleep 1秒时，控制转移到内核再到主线程，主线程exit后，进程的所有线程结束
    // exit(0); //line:conc:hellobug:exit
    //B. 使用pthread_exit退出当前线程
    pthread_exit(NULL);
    //B. pthread_cancel是一个线程向另一个线程发出，无法对自己使用
    // pthread_cancel(pthread_self());
}

/* Thread routine */
void *thread(void *vargp) 
{
    Sleep(1);
    printf("Hello, world!\n"); 
    return NULL;
}
/* $end hellobug */
