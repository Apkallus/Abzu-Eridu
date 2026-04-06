#include<stdio.h>
#include<math.h>
int main(void){
	
	int amount,n1,n2,n5,count=0;
	scanf("%d",&amount);	
	
	for(int n5=amount/5;n5>=1;n5--){
		for(int n2=amount/2;n2>=1;n2--){
			n1=amount-n5*5-n2*2;
			if(n5>=1&&n2>=1&&n1>=1){
				printf("fen5:%d, fen2:%d, fen1:%d, total:%d\n",n5,n2,n1,n5+n2+n1);
				count++;
			}
		}
	}

	printf("count = %d",count);
	
	return 0;
}
