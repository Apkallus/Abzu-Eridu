/*#include<stdio.h>
int odd_ones(unsigned x){//如果x包含奇数个1则返回1
    int res=0;

    printf("x=%d,%d\n",x,res);
}
int main(void){
    
    odd_ones();
    odd_ones();
    return 0; 
}
*/
/*
 * odd-ones.c
 */
#include <stdio.h>
#include <assert.h>
//类似二分法 利用1^1=0特性的同时
//使用低位异或高位，最终异或全位，如果最后为1，则是偶数
//尝试模拟少量位的计算后扩展到多位
int odd_ones(unsigned x) {
  x ^= x >> 16;
  x ^= x >> 8;
  x ^= x >> 4;
  x ^= x >> 2;
  x ^= x >> 1;
  x &= 0x1;
  return x;
}

int main(int argc, char* argv[]) {
  assert(odd_ones(0x10101011));
  assert(!odd_ones(0x01010101));
  return 0;
}
