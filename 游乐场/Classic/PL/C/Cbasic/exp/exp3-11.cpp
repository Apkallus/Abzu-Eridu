#include<stdio.h>
#include<math.h>
int main(void){
	
	int rq,car,sv;
	double rprice=0,dc=0,amount=0;
	scanf("%d%d",&rq,&car);
	getchar();
	sv=getchar();
	if(car==90){
		rprice=6.95;
	}if(car==93){
		rprice=7.44;
	}if(car==97){
		rprice=7.93;
	}
	if(sv=='m'){
		dc=0.05;
	}else if(sv=='e'){
		dc=0.03;
	}
	amount=rq*rprice*(1-dc);
	printf("%.2lf",amount);
	
	return 0;
}
