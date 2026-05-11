#include "csapp.h"
void *thread(void *vargp);

int main(int argc, char *argv[]){

    
    int n = atoi(argv[1]);
    pthread_t tid[n];
    
    for(int i=0; i<n; i++)
        Pthread_create(&tid[i], NULL, thread, NULL);
    for(int i=0; i<n; i++)
        pthread_join(tid[i], NULL);

    return 0;
}

void *thread(void *vargp){
    printf("Hellow, world!\n");
    return NULL;
}