#include<stdio.h>
int main(void){

    int i,n,sum=0;
    double avg;
    for(i=1;i<=4;i++){
        scanf("%d",&n);
        sum+=n;
    }
    avg=sum/4.0;
    printf("Sum = %d; Average = %.1lf",sum,avg);

    return 0;
}