#include<stdio.h>
#include<math.h>
int main(void){
	
	double sum,rate;
	int money,year;
	
	printf("enter rate");
	scanf("%lf",&rate);
	
	printf("enter money");
	scanf("%d",&money);
	
	printf("enter year");
	scanf("%d",&year);
	
	sum=money*pow(1+rate,year);
	printf("sum=%.2f",sum);
	
	return 0;
}
