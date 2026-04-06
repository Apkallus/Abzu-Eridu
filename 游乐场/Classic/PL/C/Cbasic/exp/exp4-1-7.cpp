#include<stdio.h>
#include<math.h>
int main(void){
	
	int a,n,sum=0,item=0;
	scanf("%d%d",&a,&n);	
	
	for(int i=1;i<=n;i++){
		item=item*10+a;
		sum=sum+item;
	}
	printf("s = %d",sum);
	
	return 0;
}
