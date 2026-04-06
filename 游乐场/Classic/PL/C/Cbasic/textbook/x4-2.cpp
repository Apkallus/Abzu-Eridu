#include<stdio.h>
#include<stdlib.h>
#include<math.h>
double fact(int n);
int main(void){
	
	double sum,item,fenzi,fenmu,x;
	int i;
	scanf("%lf",&x);
	
	sum=1;
	item=fenzi=i=1;
	
	while(fabs(item)>=0.00001){
		fenzi=pow(x,i);
		fenmu=fact(i);
		item=fenzi/fenmu;
		sum=sum+item;
		i++;
	}
	
	printf("%.4f",sum);
	
	return 0;
}

double fact(int n){
	
	int i;
	double res=1;
	for(i=1;i<=n;i++){
		res=res*i;
	}
	
	return res;
}
