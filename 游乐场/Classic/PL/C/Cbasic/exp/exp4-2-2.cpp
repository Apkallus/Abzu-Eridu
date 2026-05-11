#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	double sum=1,item=1;
	for(int i=1;i<=n;i++){
		item=item*i;
		sum=sum+1/item;
	}
	printf("%.8lf",sum);
	
	return 0;
}
