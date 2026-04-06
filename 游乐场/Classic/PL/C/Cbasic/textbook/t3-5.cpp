#include<stdio.h>
int main(void)
{
	int i,n,p=0;
	scanf("%d",&n);

	if(n>=2001&&n<=2100){
		for(i=2001;i<=n;i++){
			if((i%4==0&&i%100!=0)||(i%400==0)){
				p=1;
				printf("%d\n",i);
			}
		}
		if(p==0){
			printf("None");
		}
	}else{
		printf("Invalid year!");
	}

	
	return 0;
}
