#include<stdio.h>
int fib(int g){
	switch(g){
		case 0:return 0;
		case 1:
		case 2:return 2;
	}
	printf("g=%d,",g);
	return fib(g-1)+fib(g-2);
}
int main(void){
	
	int k;
	k=fib(4);
	printf("k=%ld\n",k);
	return  0;
}
