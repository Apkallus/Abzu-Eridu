#include<stdio.h>
int main(void){
	
	int a,n;
	scanf("%d%d",&a,&n);
	
	double sum=0,item=0;
	int i;
	for(i=1;i<=n;i++){
		item=item*10+a;
		sum=sum+item;	
	}
	
	printf("s = %.0f",sum);
	
	return 0;
}
