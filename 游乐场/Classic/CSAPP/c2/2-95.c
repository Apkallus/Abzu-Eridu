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
    unsigned fraclastkeepbit=frac&0x2;
    unsigned res;
    if(!(exp^0xFF)){//exp全为1的特殊值返回f
        res=f;
    }else{
        /*
        在规格化时如果阶码减少后>0还在阶码范围 则保持小数，只减阶码
        如果阶码减少后为0，则将小数+隐藏的1 并入非规格处理
        在非规格化时加可能的偏置后右移
        */
        if(exp>1){
            exp=exp-1;
        }else{
            if(exp){
                f=f+(1<<23);
                exp=0;
            }
            if(fraclastkeepbit){//只在保留的位为1时加舍入偏置向0做偶数舍入
                frac=frac+1;
            }
            f=f>>1;            
        }

        if(fraclastkeepbit){//只在保留的位为1时加舍入偏置向0做偶数舍入
            frac=frac+1;
        }
        
        res=(sign<<31)|(exp<<23)|f;
    }
    return res;
}