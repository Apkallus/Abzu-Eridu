#include<stdio.h>
int main(void){

    //将十进制转为十六进制的BCD数 
    int n10,n16=0,s=1;
    scanf("%d",&n10);
    while(n10){
        n16=n16+s*(n10%16);//直接对应高低位后输出
        n10/=16;
        s*=10;
    }

    printf("%d",n16);

    

    return 0;
}