#include<stdio.h>
#include<math.h>
int main(void){
	

	double x,y;	
	scanf("%lf%lf",&x,&y);
	
	if(x!=10){
		y=x;
	}else{
		y=1/x;
	}
	
	printf("f(%.1lf) = %.1lf",x,y);
	
	return 0;
}
