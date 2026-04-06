#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

int main(void){
	
	int n,a[2][1000],count=0,num;
	scanf("%d",&n);	
	memset(a,0,sizeof(a));
	for(int i=1;i<=n;i++){
		scanf("%d",&num);
		
		if(count==0){
			count++;
			a[0][count-1]=num;
			a[1][count-1]=1;		
		}else{
			int exist=0;
			for(int k=0;k<=count-1;k++){
				if(a[0][k]==num){
					a[1][k]++;
					exist=1;
					break;
				}
			}
			if(exist==0){
				count++;
				a[0][count-1]=num;
				a[1][count-1]=1;
			}
		}
	}
	int maxi=0;
	for(int i=1;i<=count-1;i++){
		if(a[1][i]>a[1][maxi]){
			maxi=i;
		}
	}
	printf("%d %d",a[0][maxi],a[1][maxi]);
	
	return 0;
}
