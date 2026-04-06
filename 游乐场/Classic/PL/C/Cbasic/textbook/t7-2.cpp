#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	int a[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
	}
	
	for(int i=0;i<=(n-1)/2;i++){
		int temp=a[i];
		a[i]=a[n-1-i];
		a[n-1-i]=temp;
	}
	for(int i=0;i<=n-1;i++){
		if(i==0){
			printf("%d",a[i]);
		}else{
			printf(" %d",a[i]);
		}
	}
	
	return 0;
}
