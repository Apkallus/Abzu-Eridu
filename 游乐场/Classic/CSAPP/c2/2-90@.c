#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
#include<math.h>
float u2f(unsigned x) {
    float res=*(float*)&x;
    printf("u2f=%x\n",res);
    return res;
}
//计算2的x次幂
float fpwr2(int x){
    unsigned exp,frac;
    unsigned u;
    int n=23,k=8,bias=127;

    if(x<-n-pow(2,k-1)+2){//x太小 返回0.0 小于最小非规格
        exp=0;
        frac=0;
    }else if(x<-pow(2,k-1)+2){//非规格 小于最小规格 不确定，需重新考虑
        exp=0;
        frac=1<<(x+126+n) ;//x=1-bias+fe fe=x-(-126) fe为小数位的负幂 n-fe= 左移1的位置
    }else if(x<pow(2,k)-1){//规格 小于阶码全1尾数全0
        exp=x+bias;//x=E=e-bias e=x+bias
        frac=0;
    }else{//x太大 返回正无穷
        exp=0xFF;
        frac=0;
    }

    u=exp<<23|frac;
    return u2f(u);
}


int main(int argc, char* argv[]) {//断言例子似乎错误
    printf("main=%x\n",powf(2,100));
//    assert(fpwr2(0) == powf(2,0));
    assert(fpwr2(100) == powf(2,100));
    assert(fpwr2(-100) == powf(2,-100));
    assert(fpwr2(10000) == powf(2,10000));
    assert(fpwr2(-10000) == powf(2,-10000));
    return 0;
}
  