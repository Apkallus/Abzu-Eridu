#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
unsigned f2u(float x) {
  //#答案测试 改变指针类型来解释位 而不是作为值的变化而改变位格式
    return *(unsigned*)&x;
  }
int float_le(float x,float y){
    //测试x<=y
    unsigned ux=f2u(x);
    unsigned uy=f2u(y);
    printf("%x %x,%x %x\n",x,ux,y,uy);
    unsigned sx=ux>>31;
    unsigned sy=uy>>31;
    //浮点数使用符号位表示正负
    //如果均为负 数值越大越小 ux-uy不溢出 uy-ux溢出
    //sx&sy=1 (uy-ux)>>31=1

    //如果均为正 数值越大越大 ux-uy溢出
    //!(sx|sy)=1 (ux-uy)>>31=1

    //如果符号不同 正数大 当sy=0 x更小
    //sx^sy=1 !sy=1

    //相等
    //ux^uy=0 !(ux^uy)=1
    //正负0 左移去掉符号位后=0 !0=1
    //!(ux<<31)&!(uy<<31)
    return (sx&sy&((uy-ux)>>31))|(!(sx|sy)&((ux-uy)>>31))|(sx^sy&!sy)|(!(ux^uy))|!(ux<<31)&!(uy<<31);
}
int main(int argc, char* argv[]) {
    assert(float_le((float)-0.0, (float)+0.0));//答案测试样本选择错误，传递+-0时作为int均为0 应当传递+-0.0
    assert(float_le((float)+0.0, (float)-0.0));//此处测试样本均传递int，已修改位float
    assert(float_le((float)0.0, (float)3.0));
    assert(float_le((float)-4, (float)-0.0));
    assert(float_le((float)-4.0, (float)4.0));
    return 0;
  }