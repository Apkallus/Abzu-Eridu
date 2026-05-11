#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int i,total;
	total=1;
	for(i=1;i<=n-1;i++){
		total=(total+1)*2;
	}
	printf("%d",total);
	return 0;
}
