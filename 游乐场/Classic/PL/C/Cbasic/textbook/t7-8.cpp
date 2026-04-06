#include<stdio.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	
	int narray[6][6];
	for(int row=0;row<=n-1;row++){
		for(int col=0;col<=n-1;col++){
			scanf("%d",&narray[row][col]);
		}
	}


	for(int row=0;row<=n-1;row++){
		for(int col=0;col<=n-1;col++){
			if(col+n-(m%n)<=n-1){
				printf("%d ",narray[row][col+n-(m%n)]);
			}else{
				printf("%d ",narray[row][col-(m%n)]);
			}
			
		}
		printf("\n");
	}
	
	return 0;
}
