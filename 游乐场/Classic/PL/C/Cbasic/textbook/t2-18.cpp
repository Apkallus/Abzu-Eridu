#include<stdio.h>
int main(void){
	double fact(int n);
	
	int n,m,i;
	double res;
	
	printf("enter n:");
	scanf("%d",&n);
	printf("enter m:");
	scanf("%d",&m);
	
	if(m<=n){
		res=fact(n)/(fact(m)*fact(n-m));
		printf("m=%d,n=%d,C=%.0f",m,n,res);
	}else{
		printf("er");
	}

	
	return 0;
}

double fact(int n){
	int i;
	double pro;
	
	pro=1;
	for(i=1;i<=n;i++){
		pro=pro*i;
	}
	
	return pro;
}
