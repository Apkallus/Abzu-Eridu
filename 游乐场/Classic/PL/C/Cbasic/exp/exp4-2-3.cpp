#include<stdio.h>
#include<math.h>
int is(int num);
int main(void){
	
	long int n,p,q;
	scanf("%ld",&n);	
	for(int i=2;i<=n-2;i++){
		if(is(i)&&is(n-i)){
			p=i;
			q=n-i;
			break;
		}
	}
	printf("%d = %d + %d",n,p,q);
	return 0;
}

int is(int num){
	int res=1;
	for(int i=2;i<=sqrt(num);i++){
		if(num%i==0){
			res=0;
			break;
		}
	}
	
	return res;
}
