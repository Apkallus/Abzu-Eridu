#include<stdio.h>
#include<math.h>
int main(void){
	

	double dl,cost;	
	scanf("%lf",&dl);
	
	if(dl<0){
		printf("Invalid Value!");
	}else{
		if(dl<=50){
			cost=0.53*dl;
		}else{
			cost=0.53*50+(dl-50)*(0.53+0.05);
		}
		printf("cost = %.2lf",cost);
	}
	

	
	return 0;
}
