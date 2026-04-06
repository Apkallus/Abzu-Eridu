#include<stdio.h>
int main(void){

    int n,dn;
    char tab[3]={'A','B','C'};
    int array[3];
    for(int i=0;i<=2;i++){
        scanf("%d",&array[i]);
    }
    int count;
    for(int i=0;i<=2;i++){
        count=0;
        for(int k=0;k<=2;k++){
            if(array[i]==array[k]){
                count++;
            }
        }
        if(count==1){
            printf("%c",tab[i]);
            break;
        }
    }
    return 0;
}