#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	long int sum=0;
	for(int i=1;i<=n;i++){
		sum+=pow(2,i);
	}
	printf("result = %ld",sum);
	
	return 0;
}
