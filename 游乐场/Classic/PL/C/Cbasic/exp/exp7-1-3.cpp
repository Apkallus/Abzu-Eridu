#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	int array[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",&array[i]);
	}
	
	if(n!=1){
		for(int i=0;i<=(n-1)/2;i++){
			int temp=array[i];
			array[i]=array[n-1-i];
			array[n-1-i]=temp;
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
