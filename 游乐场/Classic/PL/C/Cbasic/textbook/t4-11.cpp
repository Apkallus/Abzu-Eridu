#include<stdio.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	
	int i,j,count,sum;
	sum=count=0;
	for(i=m;i<=n;i++){
		for(j=2;j<=i/2;j++){
			if(i%j==0){
				break;
			}
		}
		if(j>i/2&&i!=1){
			count++;
			sum=sum+i;
		}
		
	}
	printf("%d %d",count,sum);
	
	return 0;
}
