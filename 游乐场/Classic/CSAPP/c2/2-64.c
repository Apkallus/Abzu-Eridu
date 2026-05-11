#include<stdio.h>
#include <assert.h>

int any_odd_one(unsigned x){
    int mask=0xAAAAAAAA;
    int res=!!(mask&x);
    printf("%.8x,%d\n",x,res);
    return res;
}
int main(void){

    int n;
    any_odd_one(0x2);
    any_odd_one(0x4);
    assert(any_odd_one(0x2));
    assert(!any_odd_one(0x4));
    return 0;
}