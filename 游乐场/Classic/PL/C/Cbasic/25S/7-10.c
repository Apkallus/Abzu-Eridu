#include<stdio.h>
int main(void){

    int a,b;
    scanf("%d%d",&a,&b);
    char op[4]={'+','-','*','/'};
    for(int i=0;i<=3;i++){
        printf("%d %c %d = ",a,op[i],b);
        switch(op[i]){
            case '+':
                printf("%d",a+b);
                break;
            case '-':
                printf("%d",a-b);
                break;
            case '*':
                printf("%d",a*b);
                break;
            case '/':
                if(a%b==0){
                    printf("%d",a/b);
                }else{
                    printf("%.2lf",1.0*a/b);
                }
                break;
        }
        putchar('\n');
    }
    return 0;
}