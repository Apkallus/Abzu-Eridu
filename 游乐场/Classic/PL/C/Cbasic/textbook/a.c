#include <stdio.h>

int main(void){

    int a[3][2];
    for(int row=0;row<=2;row++){
    	for(int col=0;col<=1;col++){
    		scanf("%d",&a[row][col]);
		}
	}
	
	for(int row=0;row<=3-1;row++){
    	for(int col=0;col<=2-1;col++){
    		printf("%d ",&a[row][col]);
		}
		printf("\n");
	}
    return 0;
}
