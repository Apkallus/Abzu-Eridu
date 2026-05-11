#include<stdio.h>
#include<math.h>
#define PI 3.141592654
double vol_ball(void){
	double r;
	printf("r:");
	scanf("%lf",&r);
	return(4.0/3.0*PI*r*r*r);
}
double vol_cylind(void){
	double r,h;
	printf("r,h:");
	scanf("%lf%lf",&r,&h);
	return(PI*r*r*h);
}
double vol_cone(void){
	double r,h;
	printf("r,h:");
	scanf("%lf%lf",&r,&h);
	return(PI*r*r*h/3.0);
}
