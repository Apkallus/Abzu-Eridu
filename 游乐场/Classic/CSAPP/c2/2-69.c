#include<stdio.h>
#include <assert.h>
int sizeus=sizeof(int)<<3;

unsigned rotate_left(unsigned x,int n){//循环左移
    unsigned res;
    unsigned isn0mask=!n-1;//排除n为0
    unsigned leftover=x>>(sizeus-n)&isn0mask;//之前写为sizeus-1-n 当n=1时，31位只移动到1位而不是0
    res=(x<<n)|leftover;//无符号右移无需用mask去掉高位的1
    
    printf("x=%x,n=%d,res=%x\n",x,n,res);
    return res;
}
int main(void){
    int x=0x12345678;
    rotate_left(x,4);
    rotate_left(x,20);
    rotate_left(x,0);
    assert(rotate_left(0x12345678, 4) == 0x23456781);
    assert(rotate_left(0x12345678, 20) == 0x67812345);
    return 0;
}