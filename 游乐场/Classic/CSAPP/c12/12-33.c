/* $begin tfgetsmain */
#include "csapp.h"
#include <sys/time.h>
#include <setjmp.h>


char *tfgets(char *s, int size, FILE *stream);
void *thread_gets(void *vargp);
void *thread_sleep(void *vargp);
/* $end tfgetsmain */

struct temp {
    char *s;
    int size;
    FILE *stream;
    pthread_t *tid_ptr;
};
sem_t mutex;


char *tfgets(char *s, int size, FILE *stream){
    
    void *res;
    pthread_t tid[2]; 
    struct temp t;
    t.s = s;
    t.size = size;
    t.stream = stream;
    t.tid_ptr = tid;

    Sem_init(&mutex, 0, 1);
    //创建两个线程，一个计时，一个读取
    //最先响应的结束另一个
    //主线程回收其他线程并判断返回值
    //似乎线程被终止则第二参数为负值
    //那么根据是否为负值判断是否为NULL
    Pthread_create(&tid[0], NULL, thread_sleep, &t);
    Pthread_create(&tid[1], NULL, thread_gets, &t);

    Pthread_join(tid[0], NULL);
    Pthread_join(tid[1], &res);

    if((long)res < 0){
        res = NULL;
    }
    return (char *)res;
}

void *thread_sleep(void *vargp){
    struct temp *p = (struct temp *)vargp;
    sleep(2);
    P(&mutex);
    pthread_cancel(p->tid_ptr[1]);
    V(&mutex);
}
void *thread_gets(void *vargp){
    struct temp *p = (struct temp *)vargp;
    char *res;
    res = fgets(p->s, p->size, p->stream);  
    P(&mutex);
    pthread_cancel(p->tid_ptr[0]);
    V(&mutex);
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