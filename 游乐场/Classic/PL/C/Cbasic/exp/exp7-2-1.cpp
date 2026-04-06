#include<stdio.h>
#include<math.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);	
	int a[6][6];
	for(int i=0;i<=m-1;i++){
		for(int k=0;k<=n-1;k++){
			scanf("%d",&a[i][k]);
		}
	}
	
	for(int i=0;i<=m-1;i++){
		int sum=0;
		for(int k=0;k<=n-1;k++){
			sum+=a[i][k];
		}
		printf("%d\n",sum);
	}
	
	return 0;
}
