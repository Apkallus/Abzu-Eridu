#include<stdio.h>
#include<assert.h>
typedef unsigned packed_t;
int sizeint=sizeof(int)<<3;

int xbyte(packed_t word, int bytenum){
    int num=(word>>(bytenum<<3))&0xFF;//把目标字节移动到最低位后mask 0xFF
    int flag=num>>7<<sizeint-1>>sizeint-8;
    int res=num|flag;
    return res;
}
int main(void){
    assert(xbyte(0x00112233, 0) == 0x33);
    assert(xbyte(0x00112233, 1) == 0x22);
    assert(xbyte(0x00112233, 2) == 0x11);
    assert(xbyte(0x00112233, 3) == 0x00);
  
    assert(xbyte(0xAABBCCDD, 0) == 0xFFFFFFDD);
    assert(xbyte(0xAABBCCDD, 1) == 0xFFFFFFCC);
    assert(xbyte(0xAABBCCDD, 2) == 0xFFFFFFBB);
    assert(xbyte(0xAABBCCDD, 3) == 0xFFFFFFAA);

    return 0;
}