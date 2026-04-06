#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	
	int array[10];
	for(int i=0;i<=n-1;i++){
		scanf("%d",&array[i]);
	}
	int x;
	scanf("%d",&x);

	int i;
	for(i=0;i<=n-1;i++){
		if(x<array[i]){
			for(int k=n-1;k>=i;k--){
				array[k+1]=array[k];
			}
			array[i]=x;
			break;
		}
	}
	if(i>n-1){
		array[n-1+1]=x;
	}

	for(int i=0;i<=n-1+1;i++){
		printf("%d ",array[i]);
	}	
	return 0;
}
