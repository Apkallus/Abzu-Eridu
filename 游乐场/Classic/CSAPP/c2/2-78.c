#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;

int divide_power2(int x,int k){// x除 2的k次幂 舍入
    int res;
    int sr=(1<<k)-1;//舍入偏置
    x=x+sr;
    res=x>>k;
    return res;
}
int main(int argc, char* argv[]) {
    int x = 0x80000007;
    assert(divide_power2(x, 1) == x / 2);
    assert(divide_power2(x, 2) == x / 4);
    return 0;
}