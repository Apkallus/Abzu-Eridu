#include<stdio.h>
int main(void){
	
	int fenmu,i,n;
	double item,sum;
	
	printf("enter n:");
	scanf("%d",&n);
	
	sum=0;
	fenmu=1;
	
	for(i=1;i<=n;i++){
		item=1.0/fenmu;
		sum=sum+item;
		fenmu=fenmu+2;
	}
	
	printf("n=%d sum=%f",n,sum);
	
	return 0;
}
