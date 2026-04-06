#include <stdio.h>
#include "csapp.h"
//不够满意 19/20/21
#define LIMIT 100000
#define PEOPLE 12

static int readtimes;
static int writetimes;
static int readcnt;
static int read_waitcnt;
static int write_waitcnt;

sem_t mutex, w, w_mutex, res, check, writelock, readlock;

void *reader(void *vargp) {
  while (1) {

    //++ 来累加当前正在等待的读者
    P(&check);
    read_waitcnt++;
    V(&check);


    P(&mutex);
    readcnt++;
    if (readcnt == 1){
      P(&w);
    }
    V(&mutex);

        
    //-- 来减少当前正在等待的读者
    P(&check);
    read_waitcnt--;
    // 如果当前无等待的读者，且写者正在等待则释放读者锁
    if(read_waitcnt == 0 && write_waitcnt > 0){
      V(&readlock);
    }
    V(&check);

    /* Critical section */
    readtimes++;
    if (readtimes == LIMIT) {
      printf("read/write: %d/%d\n", readtimes, writetimes);
      exit(0);
    }
    /* Critical section */

    P(&mutex);
    readcnt--;
    if (readcnt == 0){
      V(&w);
    }
    V(&mutex);
  }
}

void *writer(void *vargp) {
  while (1) {
    
    //如果当前存在等待的读者则加读者锁
    P(&check);
    write_waitcnt++;
    if(read_waitcnt){
      // printf("lock\n");
      V(&check);
      P(&readlock);
    }else{
      V(&check);
    }

    P(&w);

    P(&check);
    write_waitcnt--;
    V(&check);
      /* Critical section */
      writetimes++;


        /* Critical section */

    V(&w);
  }


  // }
}

void init(void) {
  readcnt = 0;
  readtimes = 0;
  writetimes = 0;
  write_waitcnt = 0;
  Sem_init(&w, 0, 1);
  Sem_init(&mutex, 0, 1);
  Sem_init(&w_mutex, 0, 1);
  Sem_init(&res, 0, 1);
  Sem_init(&check, 0, 1);
  Sem_init(&writelock, 0, 1);
  Sem_init(&readlock, 0, 1);
}


int main(int argc, char* argv[]) {
  int i;
  pthread_t tid;

  init();

  for (i = 0; i < PEOPLE; i++)
    if (i%2 == 0)
      Pthread_create(&tid, NULL, reader, NULL);
    else
      Pthread_create(&tid, NULL, writer, NULL);

  Pthread_exit(NULL);
  exit(0);
}
