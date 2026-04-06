#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,x,num,flag=0;
	scanf("%d%d",&n,&x);	
	for(int i=0;i<=n-1;i++){
		scanf("%d",&num);
		if(num==x){
			printf("%d",i);
			flag=1;
		}
	}
	if(flag==0){
		printf("Not Found");
	}
	
	return 0;
}
