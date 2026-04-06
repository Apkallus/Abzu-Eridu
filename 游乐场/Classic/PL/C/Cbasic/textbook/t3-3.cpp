#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int i;
	int sc,total=0,count=0;
	for(i=1;i<=n;i++){
		printf("enter #%d:\n",i);
		scanf("%d",&sc);
		total=total+sc;
		if(sc>=60){
			count=count+1;
		}
	}
	double avg;
	if(n==0){
		avg=0;
	}else{
		avg=1.0*total/n;
	}

	printf("avg=%.0f,count=%d",avg,count);

	return 0;
}
