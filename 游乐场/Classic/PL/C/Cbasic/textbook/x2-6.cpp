#include<stdio.h>
double fact(int n);
int main(void){

	int i,n;
	double e=0;
	printf("enter n:");
	scanf("%d",&n);
	
	
	for(i=1;i<=n;i++){
		e=e+fact(i);
	}
	printf("n=%d,e=%.0f",n,e);
	
	return 0;
}


double fact(int n){
	int i;
	double res;
	
	res=1;
	for(i=1;i<=n;i++){
		res=res*i;
	}
	
	return res;
}
