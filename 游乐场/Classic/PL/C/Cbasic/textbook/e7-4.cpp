#include<stdio.h>
int main(void){
	
	int a[10],n;
	scanf("%d",&n);
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
	}
	int minindex=0;
	for(int i=1;i<=n-1;i++){
		if(a[i]<a[minindex]){
			minindex=i;
		}
	}
	printf("min=%d,minindex=%d\n",a[minindex],minindex);
	
/*	int temp;
	temp=a[minindex];
	a[minindex]=a[0];
	a[0]=temp;

*/
	if(minindex!=0){
		a[0]^=a[minindex]^=a[0]^=a[minindex];
	}
	for(int i=0;i<=n-1;i++){
		printf("%d ",a[i]);
	}
	return 0;
}
