#include<stdio.h>
double p(int n,double x);
int main(void){
	int n;
	double x,res;
	
	printf("enter n,x:");
	scanf("%d%lf",&n,&x);
	res=p(n,x);
	printf("P(%d,%.2lf)=%.2lf\n",n,x,res);
	
	return 0;
}

double p(int n,double x){
//	p(n,x)=((2*n-1)*p(n-1,x)-(n-1)*p(n-2,x))/n;
	double res;
	if(n==0){
		res=1;
	}else if(n==1){
		res=x;
	}else{
		res=((2*n-1)*p(n-1,x)-(n-1)*p(n-2,x))/n;
	}
	
//	return p(n,x);
	return res;
}
