/*#include<stdio.h>
int leftmost_one(unsigned x){//生成x最左侧1的掩码
    int res=0;
    
    printf("x=%d,%d\n",x,res);
}
int main(void){
    
    leftmost_one();
    leftmost_one();
    return 0; 
}
// 011010
// 100101
// */
#include <stdio.h>
#include <assert.h>

/*
 * Generate mask indicating leftmost 1 in x. Assume w=32
 * For example, 0xFF00 -> 0x8000, and 0x6000 -> 0x4000.
 * If x = 0, then return 0
 */
int leftmost_one(unsigned x) {
  /*
   * first, generate a mask that all bits after leftmost one are one
   * e.g. 0xFF00 -> 0xFFFF, and 0x6000 -> 0x7FFF
   * If x = 0, get 0
   */
  //x| x逐渐加倍的位移创造高位后的位全为1
  //尝试模拟少量位的计算后扩展到多位
  x |= x >> 1;
  x |= x >> 2;
  x |= x >> 4;
  x |= x >> 8;
  x |= x >> 16;
  /*
   * then, do (mask >> 1) + (mask && 1), in which mask && 1 deals with case x = 0, reserve leftmost bit one
   * that's we want
   */
  //右移一位后+1得到从高位-1到最低位的进位到高位 高位1 其余位全0
  //使用的是当高位后全为1时+1得到高位的方法
  //以及类似二分的|本身在复制高位数字后加倍位移 得到高位后全为高位数字
  //当x不为0时+1
  return (x >> 1) + (x && 1);
}

int main(int argc, char* argv[]) {
  assert(leftmost_one(0xFF00) == 0x8000);
  assert(leftmost_one(0x6000) == 0x4000);
  assert(leftmost_one(0x0) == 0x0);
  assert(leftmost_one(0x1010) == 0x1000);
  return 0;
}