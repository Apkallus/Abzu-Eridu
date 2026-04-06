#include<stdio.h>
int main(void){
	
	double x,y;
	
	printf("Enter x:\n");
	scanf("=%f",x);
	if(x=10){
//		y=1/x
		y=1/x;
//	}else (x!=10){
	}else if(x!=10){
		y=x;
	}
//	printf("f(%.2f)=%.1f\n"x y);
	printf("f(%.2f)=%.1f\n",x,y);
	
	return 0;
}
