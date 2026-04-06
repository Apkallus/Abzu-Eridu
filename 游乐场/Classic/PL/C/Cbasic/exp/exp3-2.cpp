#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,res;
	scanf("%d",&n);	
	
	if(n<0){
		res=-1;
	}else if(n==0){
		res=0;
	}else{
		res=1;
	}
	
	printf("sign(%d) = %d",n,res);
	
	return 0;
}
