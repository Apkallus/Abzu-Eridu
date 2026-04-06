#include <stdio.h>
#define data_t long
#define OP *
//  6*1循环展开
/*
    展开后，即使数组元素*之间无数据相关，但累积变量sum作为关键路径仍存在数据相关的+，CPE下界为整数+的1
    循环展开没有改变浮点数据的关键路径，仍为浮点+的3
*/
int main(void){

    long length, i;
    data_t *udata, *vdata, *dest, sum = 0;
    long end = length -6;

    for(i = 0; i <= end; i+=6){
        sum = sum + udata[i] OP vdata[i];
        sum = sum + udata[i+1] OP vdata[i+1];
        sum = sum + udata[i+2] OP vdata[i+2];
        sum = sum + udata[i+3] OP vdata[i+3];
        sum = sum + udata[i+4] OP vdata[i+4];
        sum = sum + udata[i+5] OP vdata[i+5];
    }
    for(; i < length; i++){
        sum = sum + udata[i] OP vdata[i];
    }
    *dest = sum;

    return 0;
}