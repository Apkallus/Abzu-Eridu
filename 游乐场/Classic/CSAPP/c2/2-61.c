#include<stdio.h>
#include <assert.h>


int isxall1(int x){
    int res=0;
    int neg1=~0;
    res=!(x^neg1);
    printf("isxall1 %d\n",res);
    return res;
}
int isxall0(int x){
    int res=0;
    int neg1=~0;
    res=!(~x^neg1);
    printf("isxall0 %d\n",res);
    return res;
}
int isxlowall1(int x){
    int res=0;
    x=x&0xFF;
    res=!(x^0xFF);
    printf("isxlowall1 %d\n",res);
    return res;
}
int isxhighall0(int x){
    int res=0;
    x=(x>>(sizeof(int)<<3)-8)&0xFF;
    res=!x;
    printf("isxhighall0 %d\n",res);
    return res;
}
int main(void){

    int x=0x1234ff;
    printf("%.8x\n",x);
    isxall1(x);
    isxall0(x);
	isxlowall1(x);
    isxhighall0(x);


    int all_bit_one = ~0;
    int all_bit_zero = 0;
  
    assert(isxall1(all_bit_one));
    assert(!isxall0(all_bit_one));
    assert(isxlowall1(all_bit_one));
    assert(!isxhighall0(all_bit_one));
  
    assert(!isxall1(all_bit_zero));
    assert(isxall0(all_bit_zero));
    assert(!isxlowall1(all_bit_zero));
    assert(isxhighall0(all_bit_zero));
  
    // test magic number 0x1234ff
    assert(!isxall1(0x1234ff));
    assert(!isxall0(0x1234ff));
    assert(isxlowall1(0x1234ff));
    assert(isxhighall0(0x1234ff));
  
    // test magic number 0x1234
    assert(!isxall1(0x1234));
    assert(!isxall0(0x1234));
    assert(!isxlowall1(0x1234));
    assert(isxhighall0(0x1234));
	return 0;
} 