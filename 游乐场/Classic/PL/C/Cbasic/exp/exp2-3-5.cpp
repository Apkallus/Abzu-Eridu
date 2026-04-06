#include<stdio.h>
int main(void){
	
	int lower,upper;
	scanf("%d%d",&lower,&upper);
	
	if(lower<=upper){
		printf("fahr celsius\n");
		double c;
		for(int i=lower;i<=upper;i+=2){
			c=5.0*(i-32)/9.0;
			printf("%d%6.1lf\n",i,c);
		}		
	}else{
		printf("Invalid.");
	}

	return 0;
}
