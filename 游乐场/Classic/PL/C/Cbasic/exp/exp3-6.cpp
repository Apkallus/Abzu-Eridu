#include<stdio.h>
#include<math.h>
int main(void){
	
	double wages,taxrate,tax;
	scanf("%lf",&wages);	
	if(wages<=1600){
		taxrate=0;
	}else if(wages<=2500){
		taxrate=0.05;
	}else if(wages<=3500){
		taxrate=0.10;
	}else if(wages<=4500){
		taxrate=0.15;
	}else{
		taxrate=0.20;
	}
	
	if(wages>1600){
		tax=(wages-1600)*taxrate;
	}else{
		tax=0;
	}
	printf("%.2lf",tax);
	return 0;
}
