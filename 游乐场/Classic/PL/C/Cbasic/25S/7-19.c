#include<stdio.h>
int main(void){

    int yy,mm,dd;
    scanf("%d/%d/%d",&yy,&mm,&dd);
    int isr=0;
    if(yy%4==0&&yy%100!=0||yy%400==0){
        isr=1;
    }
    for(int i=1;i<mm;i++){
        if(i==1||i==3||i==5||i==7||i==8||i==10||i==12){
            dd+=31;
        }else if(i==2){
            dd+=28+isr;
        }else{
            dd+=30;
        }
    }
    printf("%d",dd);
    return 0;
}