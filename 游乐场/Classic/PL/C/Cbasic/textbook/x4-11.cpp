#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int total,month;
	int m1,m2,m3;
	month=0;
	m1=1;
	m2=0;
	m3=0;
	total=0;
	
	do{
		total=total+m1;
		month++;
		m3=m3+m2;
		m2=m1;
		m1=m3;
		printf("month=%d total=%d\n",month,total);
	}while(total<n);

	printf("%d",month);
	
	return 0;
}


