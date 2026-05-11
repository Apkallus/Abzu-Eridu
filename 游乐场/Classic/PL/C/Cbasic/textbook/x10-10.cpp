#include<stdio.h>
#include<math.h>
#define Sd(a,b,c) (a+b+c)/2
#define Aread(a,b,c) sqrt(Sd(a,b,c)*(Sd(a,b,c)-a)*(Sd(a,b,c)-b)*(Sd(a,b,c)-c))

double s(double a,double b,double c);
double area(double a,double b,double c);
int main(void){
	
	double a=3,b=4,c=5;
	printf("s=%f,area=%f\n",s(a,b,c),area(a,b,c));
	printf("s=%f,area=%f",Sd(a,b,c),Aread(a,b,c));
	
	return 0;
}

double s(double a,double b,double c){
	return (a+b+c)/2;
}
double area(double a,double b,double c){
	double sn=s(a,b,c);
	return sqrt(sn*(sn-a)*(sn-b)*(sn-c));
}
