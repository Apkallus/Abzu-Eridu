#include<stdio.h>
//int fact(int n);
//int multi(int n);
double fact(int n);
double multi(int n);
int main(void){
	int i;
	double sum,item,eps;
	
	eps=1E-6;
	sum=1;
	item=1;
	for(i=1;item>=eps;i++){
		item=fact(i)/multi(2*i+1);
		sum=sum+item;
	}

	printf("PI=%0.5lf\n",sum*2);
	
	return 0;
}
//int fact(int n){
double fact(int n){

	int i;
//	int res;
	double res;
	
	res=1;
//	for(i=0;i<=n;i++){
	for(i=1;i<=n;i++){
		res=res*i;
	}
	return res;
}

//int multi(int n){
double multi(int n){
	int i;
//	int res;
	double res;
	
	res=1;
	for(i=3;i<=n;i=i+2){
		res=res*i;
	}
	return res;
}
