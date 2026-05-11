#include<stdio.h>
int main(void){
	
	int a[6][6],i,j,m,n,sum;
	
	printf("input m,n:");
	scanf("%d%d",&m,&n);
	
	printf("Input array:\n");
	for(i=0;i<m;i++){
//		for(j=0;i<n;j++){
		for(j=0;j<n;j++){
			scanf("%d",&a[i][j]);
		}
	}
//	sum=0;
	for(i=0;i<m;i++){
		sum=0;
		for(j=0;j<n;j++){
			sum=sum+a[i][j];
		}
		printf("sum of row %d is %d\n",i,sum);
	}
	return 0;
}
