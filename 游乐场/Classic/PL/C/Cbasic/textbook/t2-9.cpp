#include<stdio.h>
int main(void){
	
	int n1,n2;
	
	printf("enter n1 n2:");
	scanf("%d%d",&n1,&n2);
	int he,cha,ji,shang;
	he=n1+n2;
	cha=n1-n2;
	ji=n1*n2;
	shang=n1/n2;
	
	printf("he=%d,cha=%d,ji=%d,shang=%d",he,cha,ji,shang);
	
	return 0;
}
