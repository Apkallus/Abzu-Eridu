#include <stdio.h>
#include <math.h>
int main(void){

    double item,eps,sum;
    int fenmu,flag;

    scanf("%lf",&eps);

    fenmu=1;
    flag=1;
    item=1;
    sum=0;
	
	if(eps==1||eps>1){
		sum=1;
	}else{
		while(fabs(item)>eps){
		    item=flag*1.0/fenmu;
		    sum=sum+item;
		    fenmu=fenmu+3;
		    flag=-flag;    
        }
	}


    printf("sum = %f",sum);

    return 0;
}
