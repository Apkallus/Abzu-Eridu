#include<stdio.h>
int main(void){

    int kwh;
	double amount;
	printf("enter kwh:");
	scanf("%d",&kwh);

    if(kwh<0){
        printf("Invalid Value!");
    }else{
        if(kwh<=50){
		    amount=0.53*kwh;
	    }else{
		    amount=0.53*50+(0.53+0.05)*(kwh-50);
	    }
        printf("cost = %.2f",amount);
    }
	
	return 0;
}
