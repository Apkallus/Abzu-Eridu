#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
int A(int k){
    int res=~0;
    int flagneg=~(sizeint-k>>sizeint-1);//如果k超过w位flagneg为0 否则为-1
    int flagsize=!(sizeint^k)-1;//如果k等于w flagsize为0 否则为-1
    k=k&flagneg&flagsize|(~flagneg&sizeint)|(~flagsize&sizeint);//如果k>=w则k=sizeint
    res=res>>k<<k;
    return res;
}
int B(int k,int j){
    unsigned res=~0;
    int jflagneg=~(sizeint-j>>sizeint-1);//
    int jflagsize=!(sizeint^j)-1;//
    j=j&jflagneg&jflagsize|(~jflagneg&sizeint)|(~jflagsize&sizeint);//
    res=res>>j;
    res=res&(res<<j);
    //使用2的高位次幂减去2的低位次幂得到中间的1或许比较简单
    //但已经写为0了，那么就保存右移时高位的0，在左移后&，来去掉高位的1
    //无符号右移得到左边的高位0，左移得到右边的低位0
    return res;
}

int main(int argc, char* argv[]) {
    assert(A(8) == 0xFFFFFF00);
    assert(B(16, 8) == 0x00FFFF00);
    return 0;
  }
  