#include<stdio.h>
int i;
int f(int x){
	return ((x>0)?f(x-1)+f(x-2):1);
}
int main(void){
	
	i=f(3);
	printf("%d",i);
	return 0;
}
