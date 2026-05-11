#include<stdio.h>
#include<math.h>
int main(void){
	
	double eps;
	scanf("%le", &eps);
	
	double sum=1,fenzi=1,fenmu=1,item=1;
	for(int i=1;item>=eps;i++){
		fenzi=fenzi*i;
		fenmu=fenmu*(2*i+1);
		item=fenzi/fenmu;
		sum=sum+item;
	}
	
	printf("PI = %.5lf",sum*2);
	
	return 0;
}
