#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;

int threeforths(int x){
    int res;
    int negmask=x>>sizeint-1;
    int negsr=(1<<2)-1;//舍入偏置
    res=x+(x<<1);
    res=res+(negsr&negmask);//+号优先级高于&
    res=res>>2;
    return res;
}

int main(int argc, char* argv[]) {
    assert(threeforths(8) == 6);
    assert(threeforths(9) == 6);
    assert(threeforths(10) == 7);
    assert(threeforths(11) == 8);
    assert(threeforths(12) == 9);
  
    assert(threeforths(-8) == -6);
    assert(threeforths(-9) == -6);
    assert(threeforths(-10) == -7);
    assert(threeforths(-11) == -8);
    assert(threeforths(-12) == -9);
    return 0;
  }
  