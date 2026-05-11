#include<stdio.h>
int main(void){
	
	int i,n,fenmu=1;
	double sum=0;
	
	scanf("%d",&n);
	for(i=1;i<=n;i++){
		sum+=1.0/fenmu;
		fenmu+=2;
	}
	printf("sum = %lf",sum);
	return 0;
}
