#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	int array[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",&array[i]);
	}
	int maxi=0;
	for(int i=1;i<=n-1;i++){
		if(array[maxi]<array[i]){
			maxi=i;
		}
	}
	printf("%d %d",array[maxi],maxi);
	
	return 0;
}
