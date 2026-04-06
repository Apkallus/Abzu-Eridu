#include<stdio.h>
#include<math.h>
#include<string.h>
void count(int a[],int num){
	do{
		a[num%10]++;
		num/=10;
	}while(num!=0);
}
int maxn(int a[]){
	int max;
	for(int i=0;i<=10-1;i++){
		if(i==0){
			max=a[i];
		}else{
			if(a[i]>max){
				max=a[i];
			}
		}
	}
	return max;
}
int main(void){
	
	int n;
	scanf("%d",&n);	
	int a[10],num;
	memset(a,0,sizeof(a));
	for(int i=1;i<=n;i++){
		scanf("%d",&num);
		count(a,num);
	}
	int maxnum=maxn(a);
	printf("%d:",maxnum);
	for(int i=0;i<=10-1;i++){
		if(a[i]==maxnum){
			printf(" %d",i);
		}
	}
	return 0;
}
