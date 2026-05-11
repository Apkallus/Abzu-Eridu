#include<stdio.h>
#include<math.h>
int main(void){
	
	double interest,money,rate,year;		
	scanf("%lf%lf%lf",&money,&year,&rate);
	
	interest=money*pow((1+rate),year)-money;
	
	printf("interest = %.2lf",interest);
	
	return 0;
}
