#include<stdio.h>
#include<math.h>
long int fact(int num);
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	double res;
	res=1.0*fact(n)/(fact(m)*fact(n-m));
	printf("result = %.0lf",res);
	
	return 0;
}

long int fact(int num){
	long int res=1;
	for(int i=1;i<=num;i++){
		res=res*i;
	}
	return res;
}
