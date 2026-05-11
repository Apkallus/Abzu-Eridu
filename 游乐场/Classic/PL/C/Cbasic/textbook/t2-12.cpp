#include<stdio.h>
int main(void){
	
	int low,up,fa;
	double ce;
	
	printf("enter low:");
	scanf("%d",&low);
	
	printf("enter up:");
	scanf("%d",&up);
	
	if(low<=up){
		printf("fa ce\n");
		for(fa=low;fa<=up;fa=fa+2){
			ce=5*(fa-32)/9.0;
			printf("%4d%6.1f\n",fa,ce);
		}
	}else{
		printf("IV");
	}
	
	return 0;
}
