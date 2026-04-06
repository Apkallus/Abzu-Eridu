#include<stdio.h>
int main(void){
	
	int n,i;
	printf("enter n");
	scanf("%d",&n);
	
	double sum=0,item;
	int flag=1,fenmu=1;
	for(i=1;i<=n;i++){
		item=flag*1.0*i/fenmu;
		sum=sum+item;
		printf("item:flag %d,fenzi %d,fenmu %d\n",flag,i,fenmu);
		flag=-flag;
		fenmu=fenmu+2;
	}
	
	printf("n=%d,sum=%.2f",n,sum);
	
	return 0;
}
