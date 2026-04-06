#include <stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	double sum,fenzi,fenmu,pfenzi;
	sum=0;
	fenzi=2; 
	fenmu=1; 
	pfenzi=1;
	
	int i;
	for(i=1;i<=n;i++){
		sum=sum+fenzi/fenmu;
		pfenzi=fenzi;
		fenzi=fenzi+fenmu;
		fenmu=pfenzi;
	}
	printf("%.2f",sum);
	
	return 0;
}
