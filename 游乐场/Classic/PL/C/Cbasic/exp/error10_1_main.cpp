#include<stdio.h>
#include<math.h>
#define PI 3.141592654
//#include "error10_1_cal.c";
#include "error10_1_cal.cpp"
//#include "error10_1_vol.c";
#include "error10_1_vol.cpp"
//#define PI 3.141592654

int main(void){
	int sel;
	
	while(1){
		printf("1.ball 2.cylind 3.cone else-exit\n");
		scanf("%d",&sel);
		if(sel<1||sel>3){
			break;
		}else{
			cal(sel);
		}
	}
	return 0;
}
