#include<stdio.h>
#include<math.h>
void fuc(long int n){
	if(n==0){
	
	}else{	
		fuc(n/10);
		printf("%d ",n%10);
	}

}
int main(void){
	
	long int n;
	scanf("%ld",&n);	
	if(n!=0){
		fuc(n);	
	}else{
		printf("%d ",n);
	}
	return 0;
}
