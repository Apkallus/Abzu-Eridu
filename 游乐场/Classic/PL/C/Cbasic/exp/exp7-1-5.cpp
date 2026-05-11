#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	int a[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",a+i);
	}
	for(int i=0;i<=n-1-1;i++){
		int maxi=i;
		for(int k=i+1;k<=n-1;k++){
			if(a[maxi]<a[k]){
				maxi=k;
			}
		}
		int t=a[i];
		a[i]=a[maxi];
		a[maxi]=t;
	}
	for(int i=0;i<=n-1;i++){
		if(i==0){
			printf("%d",*(a+i));
		}else{
			printf(" %d",*(a+i));
		}
	}
	
	return 0;
}
