#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include <assert.h>

unsigned replace_byte(unsigned x,int i,unsigned char b){
    unsigned res;
    res=x&~(0xFF<<(i<<3));//清空i字节
    res=res|(b<<(i<<3));//设置i字节为b
    return res;
}
int main(void){
	

    unsigned x,res;
    unsigned char b;
    x=0x12345678;
    b=0xAB;

    for(size_t i=0,end=sizeof(x);i<end;i++){
        res=replace_byte(x,i,b);
        printf("%x\n",res);
    }
    
    unsigned rep_0 = replace_byte(0x12345678, 0, 0xAB);
    unsigned rep_3 = replace_byte(0x12345678, 3, 0xAB);
  
    assert(rep_0 == 0x123456AB);
    assert(rep_3 == 0xAB345678);
	return 0;
} 