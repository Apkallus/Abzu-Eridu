#include<stdio.h>
//double fact(int n)
double fact(int n);
int main(void){
	int i;
	double sum;
	
//	for(i=1;i<10;i++){
	for(i=1;i<=10;i++){
		sum=sum+fact(i);
	}
	printf("1!+2!+¡¤¡¤¡¤+10!=%f\n",sum);
	
	return 0;
}
double fact(int n){
	int i;
	double result;
	result=1;
	for(i=1;i<=n;i++){
//		fact(n)=fact(i-1)*i;
		result=result*i;
	}
	return result;
}
