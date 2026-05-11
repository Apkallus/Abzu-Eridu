#include<stdio.h>
int main(void){

    double mile,res;
    int wtime;
    scanf("%lf%d",&mile,&wtime);
    if(mile<=3){
        res=10;
    }else if(mile<=10){
        res=10+(mile-3)*2;
    }else{
        res=10+7*2+(mile-10)*3;
    }
    res=res+wtime/5*2;
    printf("%.0f",res);

    return 0;
}