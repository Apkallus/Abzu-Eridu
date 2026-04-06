#include<stdio.h>
int main(void){
	
	int n,fenmu=1;
	scanf("%d",&n);
	
	double sum=0,flag=1;
	for(int i=1;i<=n;i++){
		sum+=flag*i/fenmu;
		fenmu+=2;
		flag=-flag;
	}
	printf("%.3lf",sum);

	return 0;
}
