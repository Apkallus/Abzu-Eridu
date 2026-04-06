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
            "vxorps %xmm1, %xmm1, %xmm1     # 之前在第二与第三操作数间少了一个','\n\t"
            "vucomiss %xmm1, %xmm0\n\t"
            "ja .above\n\t"
            "jb .below\n\t"
            "je .equal\n\t"
            "movl $3, %eax\n\t"
            "jmp .Done                      # 之前使用ret报错 \n\t"
            ".above: \n\t"
            "movl $2, %eax\n\t"
            "jmp .Done\n\t"
            ".below: \n\t"
            "movl $0, %eax\n\t"
            "jmp .Done\n\t"
            ".equal: \n\t"
            "movl $1, %eax\n\t"
            ".Done:\n\t                     # 使用内联汇编时编译器自动在结尾加入ret"                    
    );
}
int main(void){
    float array[3]={-1.0, 0.0, 1.0};
    for(int i=0;i<=2;i++){
        printf("%s\n",a[find_range(array[i])]);
    }
    
    return 0;
}