#include<stdio.h>
#include<math.h>
int main(void){
	
	long int n;
	scanf("%ld",&n);	
	
	int count=0,sum=0;
	while(n!=0){
		sum+=n%10;
		n/=10;
		count++;
	}
	printf("%d %d",count,sum);
	
	return 0;
}
