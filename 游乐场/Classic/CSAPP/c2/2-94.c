#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
typedef unsigned float_bits;
//偶数舍入 使用float_bits 可int与unsigned 
//关联lab floatScale2
float_bits float_twice(float_bits f){
    unsigned sign=f>>31;
    unsigned exp=(f>>23)&0xFF;
    unsigned frac=f&0x7FFFFF;
    unsigned res;
    if(!(exp^0xFF)){//exp全为1的特殊值返回f
        res=f;
    }else{
        if(exp){//规格M=1+f
            frac=frac+(1<<23);
        }
        frac=frac+frac;

        if(!exp){//exp全0时为非规格化
            if(frac>>23){//如果进位
                frac=frac-(1<<23);//减去进位
                exp=exp+1; //转为规格化
            }
        }else{//当为规格化
            frac=(frac>>1)-(1<<23);//对齐小数点后减去即将隐藏的1
            exp=exp+1;      
        }
        
        res=(sign<<31)|(exp<<23)|f;
    }
    return res;
}