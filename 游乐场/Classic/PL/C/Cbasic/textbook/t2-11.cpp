#include<stdio.h>
#include<math.h>
int main(void){
	
	double x,y;
	printf("enter x:");
	scanf("%lf",&x);
	
	if(x<0){
		y=pow(x+1,2)+2*x+1/x;
	}else{
		y=sqrt(x);
	}
	
	printf("y=f(%f)=%.2f",x,y);
	
	return 0;
}
