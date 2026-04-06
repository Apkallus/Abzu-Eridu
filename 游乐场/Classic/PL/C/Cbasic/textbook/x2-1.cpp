#include<stdio.h>
int main(void){
	
	int a,b,c,d;
	printf("enter a b c d:");
	scanf("%d%d%d%d",&a,&b,&c,&d);
	
	int sum;
	double avg;
	
	sum=a+b+c+d;
	avg=sum/4.0;
	
	printf("sum=%d,avg=%.1f",sum,avg);	
	
	return 0;
}
