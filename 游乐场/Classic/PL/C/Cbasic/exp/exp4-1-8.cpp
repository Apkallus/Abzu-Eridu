#include<stdio.h>
#include<math.h>
int main(void){
	
	double eps,fenmu=1,flag=1,item=1,sum=0;
	scanf("%lf",&eps);	
	do{		
		item=flag*1/fenmu;
		sum+=item;
		flag=-flag;
		fenmu+=3;
	}while(fabs(item)>eps);
	
	printf("sum = %lf",sum);
	
	return 0;
}
