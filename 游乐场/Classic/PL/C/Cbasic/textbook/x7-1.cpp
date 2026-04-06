#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int array[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",&array[i]);
	}
	
	
	for(int a=0;a<=n-1-1;a++){
		for(int b=a+1;b<=n-1;b++){
			if(array[a]<array[b]){
				int temp=array[a];
				array[a]=array[b];
				array[b]=temp;
			}
		}
	}
	
	for(int i=0;i<=n-1;i++){
		if(i==0){
			printf("%d",array[i]);
		}else{
			printf(" %d",array[i]);
		}
	}
	 
	return 0;
}
