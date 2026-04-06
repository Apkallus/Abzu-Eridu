#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
typedef unsigned float_bits;
//关联lab floatFloat2Int
int float_f2i(float_bits f){
    int bias=127; 
    int sign=f>>31;
    int exp=(f>>23)&0xFF;
    unsigned frac=f&0x7FFFFF;
    unsigned fraclastkeepbit=frac&0x2;
    int res;
    int E=exp-bias;
    /*
        浮点转整型，向0舍入，丢弃所有小数
        只表示负幂的非规格化为0
        如果是负数，将符号位扩展的效果相当于 取补+1
        如果是规格化 E只在大于等于23时才能使值到整数范围
    */
    if(!(exp^0xFF)){//exp全为1的特殊值返回0x80000000
        res=0x80000000;
    }else {
        if(!exp){//非规格化为0
            res=0;
        }else{//规格化
            if(E<0){//如果E无法使得V至少有一位整数
                res=0;
            }else if(E>31){//如果E的幂加小数幂 超过表示范围
                res=0x80000000;
            }else{//如果可能在表示范围
                frac=frac+(1<<23);//增加规格化隐藏的1

                if(E<=23){//如果要右移消除小数位
                    frac=frac>>(23-E);              
                }else{//如果要左移增加0
                    frac=frac<<(E-23);             
                }
                sign=sign<<31>>(30-E);//符号扩展到数前一位
                res=frac|sign;
            }  
        }
    }
    return res;
}