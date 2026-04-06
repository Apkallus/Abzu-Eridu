#include<stdio.h>
#include <assert.h>
int sizeint=sizeof(int)<<3;

unsigned fits_bits(int x,int n){//判断x是否能够被n个位表示
//x左移再右移判断值是否改变，也就是判断高位
    int range=sizeint-n;//再次写为sizeint-1-n导致错误
    //此处左移时是要把第n位，也就是角标为n-1的位移动到角标31 31-(n-1)=32-n
    int sx=x<<range>>range;
    unsigned res=!(sx^x);
    printf(" x=%x,n=%d,res=%x\n",x,n,res);
    return res;
}
int main(void){

    assert(!fits_bits(0xFF, 8));
    assert(!fits_bits(~0xFF, 8));
  
    assert(fits_bits(0b0010, 3));
    assert(!fits_bits(0b1010, 3));
    assert(!fits_bits(0b0110, 3));
  
    assert(fits_bits(~0b11, 3));
    assert(!fits_bits(~0b01000011, 3));
    assert(!fits_bits(~0b111, 3));
    return 0;
}