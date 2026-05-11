#include<stdio.h>
int main(void){
	
	int i,n;
	double sum=0;
	
	scanf("%d",&n);
	for(i=1;i<=n;i++){
		sum+=1.0/i;
	}
	printf("sum = %lf",sum);
	return 0;
}
