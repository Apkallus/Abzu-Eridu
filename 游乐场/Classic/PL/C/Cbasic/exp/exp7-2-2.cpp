#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	int a[10][10];
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			scanf("%d",&a[i][k]);
		}
	}
	int sum=0;
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			if(i!=n-1&&k!=n-1&&i!=n-1-k){
				sum+=a[i][k];
			}
		}
	}	
	printf("%d",sum);
	return 0;
}
