#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
typedef unsigned float_bits;

float_bits float_f2i(int f){
    unsigned bias=127; 
    unsigned exp;
    unsigned sign=(unsigned)f>>31;
    float_bits res,frac;
    int E,count,i;
    
    /*
        整型转浮点
        可能损失精度，但不超过浮点表示范围 向偶数舍入 
        判断整型是否为负 取符号位后将负数取补+1 再与正数合并处理 最后只需|符号位
        既然是整型，那么必然不在非规格的小数表示范围
        作为规格化浮点数 判断开头的1的位置 同时得到E的值
    */
    if(sign){
        f=~f+1;//负数时转为正数
    }

    if(!f){//如果为0返回0
        res=0;
    }else{
        //得到高位1的角标位置
        count=0;//如果1在第0位时
        for(int i=1;i<=31;i++){
            if((unsigned)f<<i>>i!=(unsigned)f){
                count=32-i;
                break;
            }
        }
        // 0110010 count=5
        E=count;
        exp=(E+bias)<<23;//得到2的幂与exp
        sign=sign<<31;
        frac=f&~(1<<count);//去掉开头的1
        if(count>23){//如果精度削减要舍入低位
            if((frac>>(count-23))&0x1)//如果最低保留位为1 则加入偏置向偶舍入
                frac=frac+(1<<(count-23));
            if((frac>>count)&0x1){//如果加入偏置后进位
                frac=(f-(1<<count))>>1;//再次去掉开头的1 
                //向右位移1模拟进位后10.xx的情况 此时小数位再多1 虽然f此时应该为0 是否位移值不变
                exp=exp+(1<<23);//exp增加
            }
            frac=frac>>(count-23);
        }else{//向左位移对齐
            frac=frac<<(23-count);
        }

        
        res=sign|exp|count;
        //或许加入偏置后进位的情况处理不当
    }

    return res;
}