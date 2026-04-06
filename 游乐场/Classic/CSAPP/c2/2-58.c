#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include <assert.h>

int main(void){
	
    int n=0x1234;
	int n1=*((char *)&n);//取地址后转换为字符指针读取基地址的一个字节
	int res=1;
	if(n1==0x12){//若基地址的第一个字节为0x12，则为大端机器
		res=0;
	}
	printf("%x,%x,%d",n,n1,res);
	assert(res);

	return 0;
} 