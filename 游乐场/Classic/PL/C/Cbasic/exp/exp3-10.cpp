#include<stdio.h>
#include<math.h>
int main(void){
	
	int speed,limit;
	scanf("%d%d",&speed,&limit);
	double diff=1.0*(speed-limit)/limit;
	if(diff<0.1){
		printf("OK");
	}else if(diff<0.5){
		printf("Exceed %.0lf%%. Ticket 200",diff*100);
	}else{
		printf("Exceed %.0lf%%. License Revoked",diff*100);
	}
	
	return 0;
}
