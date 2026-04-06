#include<stdio.h>
int main(void){
	
	double x,y;
	printf("enter x:");
	scanf("%lf",&x);
	
	if(x!=0){
		y=1/x;
	}else{
		y=0;
	}
	
	printf("y=f(%f)=%.1f",x,y);
	
	return 0;
}
