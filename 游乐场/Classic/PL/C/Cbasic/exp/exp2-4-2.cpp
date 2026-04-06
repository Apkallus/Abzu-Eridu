#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	long int res;
	for(int i=0;i<=n;i++){
		res=pow(3,i);
		printf("pow(3,%d) = %ld\n",i,res);
	}
	
	return 0;
}
