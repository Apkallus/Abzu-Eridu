#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include <assert.h>

int main(void){
	
    size_t x=0x89ABCDEF,y=0x76543210,lowcx,rescy;
	lowcx=x&0xFF;
	rescy=y&~0xFF;
	int res=lowcx|rescy;
	printf("x=%x,lowcx=%x\ny=%x,rescy=%x\nlowcx|rescy=%x",x,lowcx,y,rescy,res);
	assert(res == 0x765432EF);
	return 0;
} 