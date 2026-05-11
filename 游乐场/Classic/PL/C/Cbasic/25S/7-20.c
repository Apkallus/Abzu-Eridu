#include<stdio.h>
int main(void){

    int n,res;
    scanf("%d",&res);
    char ch;
    int errorf=0;
    while ((ch=getchar())!='='){
        scanf("%d",&n);
        switch (ch)  {
            case '+':
                res+=n;
                break;
            case '-':
                res-=n;
                break;
            case '*':
                res*=n;
                break;
            case '/':
                if(n==0){
                    errorf=1;
                    break;
                }
                res/=n;
                break;
            default:
                errorf=1;
                break;
        }
        if(errorf){
            break;
        }
    }
    if(errorf){
        printf("ERROR");
    }else{
        printf("%d",res);
    } 
    return 0;
}