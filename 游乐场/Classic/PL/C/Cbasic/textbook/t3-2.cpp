#include<stdio.h>
int main(void)
{
	int x,sign;
	scanf("%d",&x);
	
	if(x<0){
		sign=-1;
	}else if(x==0){
		sign=0;
	}else
	{
		sign=1;
	}
	
	printf("sign=%d",sign);
	
	return 0;
}
