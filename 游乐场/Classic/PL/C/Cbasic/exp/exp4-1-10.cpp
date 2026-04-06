#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	
	int n1=1,n2=0,n3=0,sum=0,count=0;
	do{
		sum=n1+n2+n3;		
		count++;
		n3+=n2;
		n2=n1;
		n1=n3;
	}while(sum<n);
	printf("%d",count);
	
	return 0;
}
