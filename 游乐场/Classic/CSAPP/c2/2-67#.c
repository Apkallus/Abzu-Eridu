#include<stdio.h>
#include <assert.h>

int bad_int_size_is_32(){//   题目代码
    int set_msb=1<<31;
    int beyond_msb=1<<32;//单次位移超出位宽
    return set_msb&&!beyond_msb;
}
int check32_32(){
    int set_msb=1<<31;
    int beyond_msb=set_msb<<1;//虽然无法超出位宽单次移动，但可多次移动判断
    int res=set_msb&&!beyond_msb;
    printf("check32_32 %d\n",res);
    return res;
}
int check32_16(){
    int set_msb=1<<15<<15<<1;
    int beyond_msb=set_msb<<1;
    int res=set_msb&&!beyond_msb;
    printf("check32_16 %d\n",res);
    return res;
}
int main(void){
    
    check32_32();
    check32_16();
    assert(check32_32());
    assert(check32_16());
    return 0; 
}
