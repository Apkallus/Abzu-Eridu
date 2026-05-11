#include<stdio.h>
#include <assert.h>

int sizeint=sizeof(int)<<3;
unsigned srl(unsigned x,int k){
    unsigned xsra=(int)x>>k;
    printf("srl before %x\n",xsra);

    int isk0=!k-1;//如果k=0，isk0=0 如果k非0，isk0=-1
    int mask=~(1<<(sizeint-1)>>k-1)&isk0;//创建符号位全为0其余为1的mask
    xsra=xsra&mask;//消除符号位
    printf("srl after %x\n",xsra);
    return xsra;
}
int sra(int x,int k){
    int xrl=(unsigned)x>>k;
    printf("sra before %x\n",xrl);

    int isk0=!k-1;
    int flag=(x>>(sizeint-1))&0x1;//取符号
    int mask=(flag<<(sizeint-1)>>k-1)&isk0;//创建符号位全为flag的mask
    xrl=xrl|mask;//添加符号位
    printf("sra after %x\n",xrl);
    return xrl;
}
int main(void){

    int x=0x12345678,k=4;
    srl((unsigned)x,k);
    sra(x,k);

    x=0x87654321;
    srl((unsigned)x,k);
    sra(x,k);

    unsigned test_unsigned = 0x12345678;
    int test_int = 0x12345678;
  
    assert(srl(test_unsigned, 4) == test_unsigned >> 4);
    assert(sra(test_int, 4) == test_int >> 4);
  
    test_unsigned = 0x87654321;
    test_int = 0x87654321;
  
    assert (srl (test_unsigned, 4) == test_unsigned >> 4);
    assert (sra (test_int, 4) == test_int >> 4);
    return 0;
}