#include <stdio.h>
#include <assert.h>
#include <limits.h>

int sizeint=sizeof(int)<<3;
int saturating_add(int x,int y){//正溢出时返回tmax 负溢出时返回tmin
    int xs=(x>>(sizeint-1));
    int ys=(y>>(sizeint-1));
    int xys=(x+y>>(sizeint-1));

    //x>0 y>0 x+y<0
    int posover=~xs&~ys&xys;
    //x<0 y<0 x+y>0
    int negover=xs&ys&~xys;
    int res=(x+y)&~posover&~negover;//返回x+y，如存在溢出则清空x+y 
    res=res|(posover&INT_MAX)|(negover&INT_MIN);//存在溢出时返回极值
    return res;
}
int main(int argc, char* argv[]) {
    assert(INT_MAX == saturating_add(INT_MAX, 0x1234));
    assert(INT_MIN == saturating_add(INT_MIN, -0x1234));
    assert(0x11 + 0x22 == saturating_add(0x11, 0x22));
    return 0;
}