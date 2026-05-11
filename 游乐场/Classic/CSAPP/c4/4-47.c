#include <stdio.h>
#define N 10
void bubble_a(long *data, long count){
    long i,last;
    for(last=count-1; last>0; last--){  // n-1 ~ 1      1 ~ n-1
        for(i=0; i<last; i++){          // 0 ~ last-1   0 ~ n-1-i
            if(data[i+1]<data[i]){
                long t=data[i+1];
                data[i+1]=data[i];
                data[i]=t;
            }
        }
    }
}
void bubble_b(long *data, long count){
    long i,last;
    for(last=count-1; last>0; last--){  
        for(i=0; i<last; i++){          
            if(*(data+i+1)<*(data+i)){
                long t=*(data+i+1);
                *(data+i+1)=*(data+i);
                *(data+i)=t;
            }
        }
    }
}
int main(void){
    long array[N]={1,4,7,2,8,9,5,3,6,0};
    bubble_b(array,N);
    for(int i=0;i<N;i++){
        printf("%ld ",array[i]);
    }
    return 0;
}