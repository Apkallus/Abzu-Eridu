#include<stdio.h>
int main(void){
    
    for(int i=1;i<=4;i++){
        for(int b=1;b<=i-1;b++){
            putchar(' ');
        }
        for(int k=i;k<=4;k++){
            putchar('*');
            if(k<=3){
                putchar(' ');
            }
        }
        if(i<=3){
            putchar('\n');
        }
    }
    
    return 0;
}