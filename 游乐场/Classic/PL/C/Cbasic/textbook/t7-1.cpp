#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int a[10],maxindex=0;
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
		if(a[i]>a[maxindex]){
			maxindex=i;
		}
	}
	printf("%d %d",a[maxindex],maxindex);
	return 0;
}
