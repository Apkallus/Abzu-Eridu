#include<stdio.h>
int main(void){
	
//	int i,j,n,x,a[n];
	int i,j,n,x,a[10];
	
	printf("n:");
	scanf("%d",&n);
	printf("enter %d num:",n);
	for(i=0;i<n;i++){
		scanf("%d",&a[i]);
	}
	printf("enter x:");
	scanf("%d",&x);
	for(i=0;i<n;i++){
		if(x>a[i]){
			continue;
		}
		j=n-1;
		while(j>=i){
//			a[j]=a[j+1];
//			j++;
			a[j+1]=a[j];
			j--;
		}
		a[i]=x;
		break;
	}
	if(i==n){
		a[n]==x;
	}
	for(i=0;i<n+1;i++){
		printf("%d ",a[i]);
	}
	return 0;
}
