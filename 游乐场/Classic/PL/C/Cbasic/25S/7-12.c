#include<stdio.h>
int main(void){

    int y,m,d;
    scanf("%d-%d-%d",&m,&d,&y);
    printf("%d-%0.2d-%0.2d",y,m,d);
    return 0;
}