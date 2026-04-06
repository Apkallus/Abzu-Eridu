#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
void *another_calloc(size_t nmemb,size_t size){//练习题2.35 乘法溢出 再次考虑乘法与加法
    void *p=NULL;
    size_t totalsize=nmemb*size;

    if(!nmemb||totalsize/nmemb==size){
        p=malloc(totalsize);
        memset(p,0,totalsize);
    }

    return p;
}
int main(int argc, char* argv[]) {
    void* p;
    p = another_calloc(0x1234, 1);
    assert(p != NULL);
    free(p);
  
    p = another_calloc(SIZE_MAX, 2);
    assert(p == NULL);
    free(p);
    return 0;
}