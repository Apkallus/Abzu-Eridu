#include<stdio.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	
	for(int row=0;row<=m-1;row++){
		int sum=0,number;
		for(int col=0;col<=n-1;col++){
			scanf("%d",&number);
			sum=sum+number;
		}
		printf("%d\n",sum);
	}
	
	return 0;
}
