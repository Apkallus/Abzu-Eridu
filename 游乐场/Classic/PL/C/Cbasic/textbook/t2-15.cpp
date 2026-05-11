#include<stdio.h>
int main(void){
	
	int fenmu,flag,i,n;
	double item,sum;
	
	printf("enter n:");
	scanf("%d",&n);
	
	flag=1;
	sum=0;
	fenmu=1;
	
	for(i=1;i<=n;i++){
		item=flag*1.0/fenmu;
		sum=sum+item;
		flag=-flag;
		fenmu=fenmu+3;
	}
	
	printf("n=%d sum=%f",n,sum);
	
	return 0;
}
