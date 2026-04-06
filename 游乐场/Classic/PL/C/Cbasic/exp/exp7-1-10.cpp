#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,a[10];
	scanf("%d",&n);	
	int mini,maxi;
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
	}
	mini=maxi=0;
	for(int i=1;i<=n-1;i++){
		if(a[mini]>a[i]){
			mini=i;
		}else if(a[maxi]<a[i]){
			maxi=i;
		}
	}

	if(a[0]==a[maxi]){
		maxi=mini;
	}
	int t;
	t=a[0];
	a[0]=a[mini];
	a[mini]=t;
	

	t=a[n-1];
	a[n-1]=a[maxi];
	a[maxi]=t;
	
	for(int i=0;i<=n-1;i++){
		printf("%d ",a[i]);
	}
	
	return 0;
}
