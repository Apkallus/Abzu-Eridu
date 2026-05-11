#include <stdio.h>
#define data_t long
#define OP *
//  6*6循环展开
/*
    循环展开且增加累积变量后
    对于整数下界仍为1
    对于浮点数，由于能够使用多个功能单元以及流水线，使得其操作周期接近1

    循环开销仍然存在
    每周期进行操作的上限
    浮点* 5*2=10 未达到
    浮点+ 3*1=3  达到
    整数* 3*1=3  达到
    整数+ 1*4=4  达到
    除浮点*外，其余操作已达到功能单元上限
*/
int main(void){

    long length, i;
    data_t *udata, *vdata, *dest, sum = 0;
    long end = length -6;
    long acc0,acc1,acc2,acc3,acc4,acc5;

    for(i = 0; i <= end; i+=6){// 要在无数据相关的值处加 ( )
        acc0 = acc0 + (udata[i] OP vdata[i]);
        acc1 = acc1 + (udata[i+1] OP vdata[i+1]);
        acc2 = acc2 + (udata[i+2] OP vdata[i+2]);
        acc3 = acc3 + (udata[i+3] OP vdata[i+3]);
        acc4 = acc4 + (udata[i+4] OP vdata[i+4]);
        acc5 = acc5 + (udata[i+5] OP vdata[i+5]);
    }
    for(; i < length; i++){//展开与剩余的循环范围不同
        acc0 = acc0 + udata[i] OP vdata[i];
    }
    *dest = acc0 + acc1 + acc2 + acc3 + acc4 + acc5;

    return 0;
}