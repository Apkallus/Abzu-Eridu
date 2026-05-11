#include<stdio.h>
#include<math.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);	
	int a[20][20],flag=0;
	for(int i=0;i<=m-1;i++){
		for(int k=0;k<=n-1;k++){
			scanf("%d",&a[i][k]);
		}
	}	
	
	for(int i=1;i<=m-1-1;i++){
		for(int k=1;k<=n-1-1;k++){
			if(a[i][k]>a[i][k-1]&&a[i][k]>a[i][k+1]&&a[i][k]>a[i-1][k]&&a[i][k]>a[i+1][k]){
				printf("%d %d %d\n",a[i][k],i+1,k+1);
				flag=1;
			}
		}
	}
	if(flag==0){
		printf("None %d %d",m,n);
	}	
	return 0;
}
