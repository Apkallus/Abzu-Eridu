#include<stdio.h>
int main(void){
	
	char x=064;
	printf("char x=%d\n",x);
	
	printf("x<<2=%d\n",x<<2);
	printf("x<<2&x=%d\n",x<<2&x);
	printf("~x=%d %c %x\n",~x^x<<2&x,~x^x<<2&x,~x^x<<2&x);
	
	return 0;
}
