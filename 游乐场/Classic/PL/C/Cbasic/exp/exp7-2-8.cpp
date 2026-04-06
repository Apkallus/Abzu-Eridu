#include<stdio.h>
#include<math.h>
int is(int a[][6],int row,int cal,int n){
	int flag=1;
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			if(a[row][cal]<a[row][k]||a[row][cal]>a[i][cal]){
				flag=0;
				break;
			}
		}
		if(flag==0){
			break;
		}
	}
	return flag;
}
int main(void){
	
	int n,a[6][6];
	scanf("%d",&n);	
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			scanf("%d",&a[i][k]);
		}
	}
	int flag=0;
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			if(is(a,i,k,n)){
				flag=1;
				printf("%d %d\n",i,k);
			}
		}
	}		
	if(flag==0){
		printf("NONE");
	}
	return 0;
}
