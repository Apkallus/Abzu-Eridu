#include<stdio.h>
int main(void){
	static int a[4][4];
	int *p[4],i,j;
	for(i=0;i<4;i++){
		p[i]=&a[i][0];
	}
	for(i=0;i<4;i++){
		*(p[i]+i)=1;
		*(p[i]+4-(i+1))=1;
	}
	for(i=0;i<4;i++){
		for(j=0;j<4;j++){
			printf("%2d",p[i][j]);
		}
		printf("\n");
	}
}
