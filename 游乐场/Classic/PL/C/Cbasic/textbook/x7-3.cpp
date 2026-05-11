#include<stdio.h>
void testfunction(void);
int main(void){
	
	int t;
	scanf("%d",&t);
	
	for(int i=1;i<=t;i++){
		testfunction();
	}
	
	return 0;
}

void testfunction(void){
	int n;
	scanf("%d",&n);
	int array[10][10],flag=1;
	for(int row=0;row<=n-1;row++){
		for(int col=0;col<=n-1;col++){
			scanf("%d",&array[row][col]);
			if(row>col&&array[row][col]!=0){
				flag=0;
			}
		}

	}
	if(flag==1){
		printf("YES\n");
	}else{
		printf("NO\n");
	}
}
