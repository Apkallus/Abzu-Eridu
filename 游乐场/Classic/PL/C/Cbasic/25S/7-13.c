#include<stdio.h>
int main(void){

    int d;
    scanf("%d",&d);
    printf("%d",(d+2)%7?(d+2)%7:7);

    return 0;
}