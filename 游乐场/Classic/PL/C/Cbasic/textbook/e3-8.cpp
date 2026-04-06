#include<stdio.h>
int main(void)
{
	int i,choice;
	double price;
	
	for(i=1;i<=5;i++){
		printf("1 cr\n");
		printf("2 p\n");
		printf("3 ch\n");
		printf("4 co\n");
		printf("0 exit\n");
		
		printf("enter choice\n");
		scanf("%d",&choice);
		
		if(choice==0)
			break;
		
		switch(choice){
			case 1:price=3.0;break;
			case 2:price=2.5;break;
			case 3:price=4.0;break;
			case 4:price=3.5;break;
			default:price=0;break;
		}
		
		printf("price=%.1f\n",price);
	}
	printf("tks\n");
	
	return 0;
}
