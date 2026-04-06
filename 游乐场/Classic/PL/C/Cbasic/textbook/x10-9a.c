#include<stdio.h>
#include"x10-9b_isres.c"
int main(void){
	
	int n;
	scanf("%d",&n);
	int count=0,i;
	for(i=1;i<=n;i++){
		int item;
		scanf("%d",&item);
		if(isres(item)){
			count++;
		}
	}
	printf("%d",count);
	
	return 0;
}


