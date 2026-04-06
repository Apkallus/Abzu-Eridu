#include<stdio.h>
int f(int n){
	int t,t0,t1;
	t0=0;t1=1;t=n;
	while(n>1){
		printf("t0=%d,t1=%d\n",t0,t1);
		t=t0+t1;
		t0=t1;
		t1=t;
		n--;
	}
	return t;
}
int main(void){
	
	printf("%d",f(4));
	
	
	return 0;
}
