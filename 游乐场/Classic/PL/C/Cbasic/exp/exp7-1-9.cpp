#include<stdio.h>
int main(void){
	
	int n,a[4];
	scanf("%d",&n);	
	for(int i=3;i>=0;i--){
		a[i]=(n%10+9)%10;
		n/=10;
	}
	
	int t;
	t=a[0];
	a[0]=a[2];
	a[2]=t;		
	
	t=a[1];
	a[1]=a[3];
	a[3]=t;	
	
	int res=0;
	for(int i=0;i<=3;i++){
		res=res*10+a[i];
	}
	printf("The encrypted number is %04d",res);

	return 0;
}

