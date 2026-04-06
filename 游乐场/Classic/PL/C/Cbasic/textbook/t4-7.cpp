#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	double sum,fenmu,item;
	int i,j;
	
	sum=1;
	for(i=1;i<=n;i++){
		fenmu=1;
		for(j=1;j<=i;j++){
			fenmu=fenmu*j;
		}
		item=1/fenmu;
		sum=sum+item;
	}
	
	printf("%.8f",sum);
	
	return 0;
}
