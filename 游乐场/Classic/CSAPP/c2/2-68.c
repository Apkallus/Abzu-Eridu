#include<stdio.h>
#include <assert.h>

int sizeint=sizeof(int)<<3;

int lower_one_mask(int n){//最小有效n位设置为1
    int res;
    int isn32=!(n^32)-1;//创建mask n=32为0000 其他情况为1111
    n=n&isn32;//在n为32时n=0确保不位移超过范围 
    res=~0;
    res=res>>n<<n;//全1右移再左移消除n个1为0后取补 或tmin右移后取补
    res=(~res)|~isn32;//将n=32的特殊值加入结果
    printf("n=%d res=%x\n",n,res);
    return res;
}
int main(void){

    lower_one_mask(6);
    lower_one_mask(17);
    lower_one_mask(32);
    assert(lower_one_mask(6) == 0x3F);
    assert(lower_one_mask(17) == 0x1FFFF);
    assert(lower_one_mask(32) == 0xFFFFFFFF);
    return 0;
}