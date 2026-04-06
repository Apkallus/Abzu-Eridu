#include<stdio.h>
#include<math.h>
int is(long int num){
	int flag=1;
	for(int i=2;i<=sqrt(num);i++){
		if(num%i==0){
			flag=0;
			break;
		}
	}
	return flag;
}
int main(void){
	
	int n,flag=0;
	double num;
	scanf("%d",&n);	
	for(int i=2;i<=n;i++){
		num=pow(2,i)-1;
		if(is(num)){
			flag=1;
			printf("%.0lf\n",num);
		}
	}
	if(flag==0){
		printf("None");
	}
	return 0;
}
