#include<stdio.h>
#include <assert.h>

int main(void){
    int res=0;

    res=~0>>(sizeof(int)<<3-1);
    res=res&1;
    printf("%d",res);
    assert(res);
    return 0;
}