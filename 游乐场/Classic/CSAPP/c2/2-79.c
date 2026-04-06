#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
int mul3div4(int x){//*3/4 1+2-4
    int res;
    int sr=(1<<2)-1;//溢出舍入偏置
    res=x+(x<<1);
    res=res+sr;
    res=res>>2;
    return res;
}
int main(int argc, char* argv[]) {
    int x = 0x87654321;
    assert(mul3div4(x) == x * 3 / 4);
    return 0;
  }
  