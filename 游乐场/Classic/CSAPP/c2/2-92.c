#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
typedef unsigned float_bits;
//偶数舍入 使用float_bits 可int与unsigned 
float_bits float_negate(float_bits f){
    unsigned sign=f>>31;
    unsigned exp=(f>>23)&0xFF;
    unsigned frac=f&0x7FFFFF;
    unsigned res;
    if(!(exp^0xFF)&&frac){//当exp全1时且frac!=0则为NaN
        res=f;
    }else{
        sign=(!sign)<<31;
        exp=exp<<23;
        res=sign|exp|frac;
    }
    return res;
}