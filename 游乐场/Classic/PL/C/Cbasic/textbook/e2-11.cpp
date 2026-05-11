#include<stdio.h>
int main(void){
	double fact(int n);
	
	int n,i;
	double res;
	
	printf("enter n:");
	scanf("%d",&n);
	
	for(i=0;i<=n;i++){
		res=fact(i);
		printf("%d!=%.0f\n",i,res);	
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
