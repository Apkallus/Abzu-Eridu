#include<stdio.h>
char *a[4]={"NEG","ZERO","POS","OTHER"};
/*
int find_range(float x){
    int res;
    if(x>0){
        res=2;
    }else if(x<0){
        res=0;
    }else if(x==0){
        res=1;
    }else{
        res=3;
    }
    return res;
}
*/
int find_range(float x){
    asm(
            "vxorps %xmm1, %xmm1, %xmm1\n\t"    
            "vucomiss %xmm1, %xmm0\n\t"
            "movl $3, %eax\n\t"
            "movl $0, %edi\n\t"
            "movl $1, %esi\n\t"
            "movl $2, %edx\n\t"    
            "cmovb %edi, %eax\n\t"
            "cmove %esi, %eax\n\t"
            "cmova %edx, %eax\n\t"                    
        );
}
int main(void){
    float array[3]={-1.0, 0.0, 1.0};
    for(int i=0;i<=2;i++){
        printf("%s\n",a[find_range(array[i])]);
    }
    
    return 0;
}