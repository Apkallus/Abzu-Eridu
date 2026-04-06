#include<stdio.h>
int main(void){
	
	int i,n,fenmu=1,flag=1;
	double sum=0;
	
	scanf("%d",&n);
	for(i=1;i<=n;i++){
		sum+=1.0*flag/fenmu;
		fenmu+=3;
		flag=-flag;
	}
	printf("sum = %.3lf",sum);
	return 0;
}
