#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
int A(int x,int y){
    //false when x=tmin -x=tmin -x<=-y
    return x<y==-x>-y;
}
int B(int x,int y){
    //17=16+1 y<<4+y
    //15=16-1 x<<4-x
    //(y<<4)+(x<<4)+y-x
    //true
    return ((x+y)<<4)+y-x==17*y+15*x;
}
int C(int x,int y){//#回答错误
    //~x=-x-1 ~y=-y-1
    //-x-1-y-1+1=-(x+y)-1=~(x+y)+1-1=~(x+y)
    //false when x or y =tmin
    //回答错误 x的加法逆元-x=~x+1 这也包括tmin
    //tmin的特殊值在于 -x=x 使得其也有x=~x+1 
    return ~x+~y+1==~(x+y);
}
int D(int x,int y,unsigned ux,unsigned uy){
    //ux-uy=-uy+ux=
    //-(uy-ux)=-u(y-x)
    //uy-ux=u(y-x)
    //true 位级表示不变
    return (ux-uy)==-(unsigned)(y-x);
}
int E(int x){
    //true 清空正权 无论正负都更小
    return ((x>>2)<<2)<=x;
}
