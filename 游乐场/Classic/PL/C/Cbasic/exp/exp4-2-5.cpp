#include<stdio.h>
#include<math.h>
int is(int num,int n);

int main(void){
	
	int n;
	scanf("%d",&n);	
	for(int i=pow(10,n-1);i<=pow(10,n)-1;i++){
		if(is(i,n)){
			printf("%d\n",i);
		}
	}
	
	return 0;
}
int is(int num,int n){
	int sum=0,flag=0,i=num;
	while(i>0){
		sum=sum+pow(i%10,n);
		i=i/10;
	}
	if(sum==num){
		flag=1;
	}
	return flag;
}
