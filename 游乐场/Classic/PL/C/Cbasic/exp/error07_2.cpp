#include<stdio.h>
int main(void){
	
	int i,x,n;
	int a[10];
	
	printf("n:");
	scanf("%d",&n);
	printf("%d num:",n);
	for(i=0;i<n;i++){
//		scanf("%d",a[i]);
		scanf("%d",&a[i]);
	}
	printf("x:");
	scanf("%d",&x);
	for(i=0;i<n;i++){
//		if(a[i]!=x){
		if(a[i]==x){
			break;
		}
	}
//	if(i!=n){
	if(i==n){
		printf("not found %d\n",x);
	}else{
		printf("%d=a[%d]=%d\n",x,i,a[i]);
	}
	return 0;
}
