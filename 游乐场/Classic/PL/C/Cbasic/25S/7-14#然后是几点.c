#include<stdio.h>
int main(void){

    int n,hh,mm,psm;
    scanf("%d%d",&n,&psm);
    hh=n/100;
    mm=n%100+psm;
    
    

    hh=(hh+mm/60)%24;//无论正负，hh处理进位借位 但只能处理60分钟倍数的借位
    if(mm<0&&mm%60){//有余数的情况下要再-1借位
        hh--;
    }        
    if(hh<0){
        hh=hh+24;
    }
    mm=mm%60; 
    if(mm<0){
        mm=mm+60;
    }
    
    printf("%0.1d%0.2d",hh,mm);
    return 0;
}