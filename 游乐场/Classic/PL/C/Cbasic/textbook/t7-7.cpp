#include<stdio.h>
int main(void){
	
	int n,array[10][10],sum=0;
	scanf("%d",&n);
	for(int row=0;row<=n-1;row++){
		for(int col=0;col<=n-1;col++){
			scanf("%d",&array[row][col]);
			if((row+col!=n-1)&&row!=n-1&&col!=n-1){
				sum=sum+array[row][col];
			}
		}
	}
	printf("%d",sum);
	return 0;
}
