#include<stdio.h>
int reverse(int n);
int main(void){
	
	int x,y;
	
	scanf("%d%d",&x,&y);
	printf("%d->%d\n",x,reverse(x));
	printf("%d->%d\n",y,reverse(y));
	
	return 0;
}

int reverse(int n){
	int m,res;
	res=0;
	if(n<0){
//		m=n;
		m=-n;
	}else{
//		m=-n;
		m=n;
	}
//	while(m==0){
	while(m!=0){
//		res=res*10+m/10;
		res=res*10+m%10;
//		m=m%10;
		m=m/10;
	}
	if(n>=0){
		return res;
	}else{
		return -res;
	}
}
