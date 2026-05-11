#include<stdio.h>
int main(void){
	
	int num=152;
	
	printf("152 = %d + %d*10 + %d*100",num%10,num/10%10,num/100%10);
	
	return 0;
}
