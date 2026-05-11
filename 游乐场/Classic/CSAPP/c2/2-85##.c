#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
/*
    k位指数与n位小数，写出阶码E 尾数M 小数f和值V的公式
    V=2^E*M    
    Bias=2^(k-1)-1
    f=2^-n*uf
    规格化                   非规格
    M=f+1                   M=f
    E=e-Bias                E=1-Bias
    V=pow(2,e-Bias)·(f+1)   =pow(2,1-Bias)·f 

*/

/*描述位表示
二进制整数到小数的转换 
移动小数点 *2的位移数量幂 去掉开头的1 就能得到浮点编码各项的值

7.0
    7.0=111.000=1.11000*2^2
    M=1.11 f=0.11 E=2 e=E+bias=2+bias v=7.0
    0 100001 110000


最大奇整数
    1111111=1.111111*2^n 
    M=1+1-2^-n f=1-2^-n E=n e=E=bias=n+bias v=2^n*(2-2^-n)=2^(n+1)-1
    0 n+bias 111111


最小的规格化数的倒数
    000001 0000
    M=1 f=0 E=1-bias
    v=2^(1-bias)

    倒数
    v=2^(bias-1)
    E=bias-1 M=1 f=0 e=bias+E=2*bias-1
    0 1111101 000
*/