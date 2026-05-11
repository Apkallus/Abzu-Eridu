#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	long int sum=0,fact=1;
	for(int i=1;i<=n;i++){
		fact=fact*i;
		sum=sum+fact;
	}
	printf("%d",sum);
	
	return 0;
}
