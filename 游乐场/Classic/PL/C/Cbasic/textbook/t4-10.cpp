#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int i,min,sc;
	scanf("%d",&sc);
	min=sc;
	for(i=1;i<=n-1;i++){
		scanf("%d",&sc);
		if(sc<min){
			min=sc;
		}
	}
	printf("min = %d",min);
	return 0;
}
