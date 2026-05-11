#include<stdio.h>
int main(void){
	
	int n;
	printf("enter n:");
	scanf("%d",&n);
	
	int i,sum=0;
	for(i=1;i<=n;i++){
		sum=sum+i;
	}
	
	printf("n=%d sum=%d",n,sum);
	
	return 0;
}
