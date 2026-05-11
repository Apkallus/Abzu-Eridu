#include<stdio.h>
#include<math.h>
int main(void){
	
	double apple=3.0,pear=2.5,orange=4.1,grape=10.2,price;
	int choice;
	printf("[1] apple\n[2] pear\n[3] orange\n[4] grape\n[0] exit\n");
	for(int i=1;i<=5;i++){
		scanf("%d",&choice);
		if(choice==0){
			break;
		}
		switch(choice){
			case 1:price=apple;break;
			case 2:price=pear;break;
			case 3:price=orange;break;
			case 4:price=grape;break;
			default:price=0;break;
		}
		printf("price = %.2lf\n",price);
	}
	
	return 0;
}
