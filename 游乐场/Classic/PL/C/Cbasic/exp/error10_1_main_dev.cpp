#include <iostream>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

#include<stdio.h>
#include<math.h>
#define PI 3.141592654
void cal(int sel);

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
