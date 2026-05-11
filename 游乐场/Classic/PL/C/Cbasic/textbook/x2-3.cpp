#include<stdio.h>
int main(void){
	
	int m,n;
	printf("enter m n:");
	scanf("%d%d",&m,&n);
	
	int i;
	double pro,res;
	res=0;
	for(i=m;i<=n;i++){
		pro=i*i+1.0/i;
		res=res+pro;
	}
	
	printf("m=%d,n=%d,res=%f",m,n,res);
	
	return 0;
}
