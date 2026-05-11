#include<stdio.h>
#include<math.h>
int main(void){
	
	int a[10],count=0,n=10;

	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
		count++;
	}
	
	for(int i=1;i<=n-1;i++){
		if(a[i]!=0){
			printf("%d",i);
			a[i]--;
			break;
		}
	}
	for(int i=0;i<=n-1;i++){
		for(int k=a[i];k>=1;k--){
			printf("%d",i);
		}
	}


	return 0;
}
