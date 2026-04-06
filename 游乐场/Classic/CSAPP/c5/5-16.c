#include <stdio.h>
#define data_t long
#define OP *
//  6*1a循环展开

int main(void){

    long length, i;
    data_t *udata, *vdata, *dest, sum = 0;
    long end = length -6;

    for(i = 0; i <= end; i+=6){
        sum = sum + 
            ((udata[i] OP vdata[i]
            +udata[i+1] OP vdata[i+1])
            +(udata[i+2] OP vdata[i+2]
            +udata[i+3] OP vdata[i+3])
            +(udata[i+4] OP vdata[i+4]
            +udata[i+5] OP vdata[i+5]));
    }
    for(; i < length; i++){
        sum = sum + udata[i] OP vdata[i];
    }
    *dest = sum;

    return 0;
}