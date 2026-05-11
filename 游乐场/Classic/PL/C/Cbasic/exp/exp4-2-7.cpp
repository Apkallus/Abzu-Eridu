#include<stdio.h>
#include<math.h>
int is(int num){
	int sum=0,flag=0;
	for(int i=1;i<=num/2;i++){
		if(num%i==0){
			sum=sum+i;
		}
	}
	if(sum==num){
		flag=1;
	}
	return flag;
}
void printperf(int num){
	printf("%d = ",num);
	int flag=0;
	for(int i=1;i<=num/2;i++){
		if(num%i==0){
			if(flag==0){
				printf("%d",i);
				flag=1;
			}else{
				printf(" + %d",i);
			}
		}
	}	
	putchar('\n');
}
int main(void){
	
	int m,n,flag=0;
	scanf("%d%d",&m,&n);
	for(int i=m;i<=n;i++){
		if(is(i)){
			printperf(i);
			flag=1;
		}
	}	
	if(flag==0){
		printf("None");
	}
	
	return 0;
}
