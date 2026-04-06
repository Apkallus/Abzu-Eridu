#include<stdio.h>
double result_real,result_imag;
void complex_prod(double x1,double y1,double x2,double y2);
int main(void){
	double imag1,imag2,real1,real2;
	
	printf("enter 1st real and imag:");
	scanf("%lf%lf",&real1,&imag1);
	printf("enter 2st real and imag:");
	scanf("%lf%lf",&real2,&imag2);
	
	complex_prod(real1,imag1,real2,imag2);
	printf("complex is %f+%fi\n",result_real,result_imag);
	
	return 0;
}

//void complex_prod(double x1,y1,x2,y2);{
void complex_prod(double x1,double y1,double x2,double y2){
//	double result_real,result_imag;
	
	result_real=x1*x2-y1*y2;
	result_imag=x1*y2+x2*y1;
	
//	return result_real,result_imag;
}
