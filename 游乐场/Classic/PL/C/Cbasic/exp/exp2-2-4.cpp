#include<stdio.h>
#include<math.h>
int main(void){
	
	int a,b,c,d,sum;
	double avg;	
	scanf("%d%d%d%d",&a,&b,&c,&d);
	sum=a+b+c+d;
	avg=sum/4.0;
	
	printf("Sum = %d; average = %.1lf",sum,avg);
	
	return 0;
}
