#include<stdio.h>
#include<math.h>
#define PI 3.141592654
void cal(int sel){
	double vol_ball(void);
	double vol_cylind(void);
	double vol_cone(void);
	
	switch(sel){
		case 1:
			printf("ball:%.2f\n",vol_ball());
			break;
		case 2:
			printf("cylind:%.2f\n",vol_cylind());
			break;
		case 3:
			printf("cone:%.2f\n",vol_cone());
			break;
	}
}
