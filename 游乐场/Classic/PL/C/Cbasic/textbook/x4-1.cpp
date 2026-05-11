#include<stdio.h>

int main(void){
	
	int n,sum=0;
	do{
		scanf("%d",&n);
		if(n<=0){
			break;
		}
		if(n%2!=0){
			sum=sum+n;
		}
	}while(1);
	printf("%d",sum);
	
	return 0;
}
