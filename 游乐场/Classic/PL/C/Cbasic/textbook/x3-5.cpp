#include<stdio.h>
#include<math.h>
int main(void){
	
	double x1,y1,x2,y2,x3,y3;
	scanf("%lf%lf%lf%lf%lf%lf",&x1,&y1,&x2,&y2,&x3,&y3);
	double a,b,c;
	
	a=sqrt(pow(x2-x3,2)+pow(y2-y3,2));
	b=sqrt(pow(x1-x3,2)+pow(y1-y3,2));
	c=sqrt(pow(x1-x2,2)+pow(y1-y2,2));	
	
	double s,area;
	if(a+b>c&&a+c>b&&b+c>a){
		s=(a+b+c)/2;
		area=sqrt(s*(s-a)*(s-b)*(s-c));
		printf("L = %.2f, A = %.2f",a+b+c,area);
	}else{
		printf("Impossible");
	}
	
	return 0;
}
