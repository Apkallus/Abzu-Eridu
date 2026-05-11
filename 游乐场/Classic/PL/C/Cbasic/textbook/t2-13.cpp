#include<stdio.h>
int main(void){
	
	int i,n;
	double item,sum;
	
	printf("enter n:");
	scanf("%d",&n);
	
	sum=0;
	
	for(i=1;i<=n;i++){
		item=1.0/i;
		sum=sum+item;
	}
	
	printf("n=%d sum=%f",n,sum);
	
	return 0;
}
