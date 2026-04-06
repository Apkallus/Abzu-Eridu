#include<stdio.h>
#define F(x) x-2
#define D(x) x*F(x)
int main(void){
	printf("%d,%d",D(3),D(D(3)));
	
	return 0;
}

