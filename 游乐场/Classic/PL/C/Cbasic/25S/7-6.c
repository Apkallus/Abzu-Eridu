#include<stdio.h>
int main(void){

    int cm;
    double m,foot,inch;
    scanf("%d",&cm);
    m=cm/100.0;
    foot=m/0.3048;
    inch=(foot-(int)foot)*12;
    foot=(int)foot;
    printf("%.0lf %d",foot,(int)inch);
    
    return 0;
}