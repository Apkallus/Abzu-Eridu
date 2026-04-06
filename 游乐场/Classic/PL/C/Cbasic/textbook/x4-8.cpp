#include<stdio.h>
int main(void){
	
	long int high,n;
	scanf("%ld%ld",&high,&n);
	
	double sum,item,fantan,pfantan;
	
	if(n!=0){
		sum=-high;
		fantan=high;	
		int i;
		for(i=1;i<=n;i++){
			fantan=fantan/2;
			sum=sum+fantan*4;
		}	
	}else{
		sum=0;
		fantan=0;
	}

	printf("%.1f %.1f",sum,fantan);
	return 0;
}
