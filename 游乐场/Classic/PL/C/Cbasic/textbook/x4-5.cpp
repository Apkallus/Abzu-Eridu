#include<stdio.h>
int main(void){
	
	int n5,n2,n1;
	int n;
	scanf("%d",&n);
	
	int m5,m2,count=0;
	m5=n/5;
	m2=n/2;
	
	n1=0;
	
	for(n5=m5;n5>0;n5--){
		for(n2=m2;n2>0;n2--){
			n1=n-5*n5-2*n2;
			if(n1>=1){
				printf("fen5:%d, fen2:%d, fen1:%d, total:%d\n",n5,n2,n1,n5+n2+n1);
				count++;
			}
		}
	}
	printf("count = %d",count);
	
	return 0;
}
