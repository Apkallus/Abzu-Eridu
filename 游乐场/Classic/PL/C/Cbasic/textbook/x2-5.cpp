#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	printf("enter n:");
	scanf("%d",&n);
	
	double sum=0,item;
	int i;
	for(i=1;i<=n;i++){
		item=sqrt(i);
		sum=sum+item;
		printf("sqrt(%d)=%.2f\n",i,item);
	}
	printf("n=%d,sum=%.2f",n,sum);
	
	return 0;
}
