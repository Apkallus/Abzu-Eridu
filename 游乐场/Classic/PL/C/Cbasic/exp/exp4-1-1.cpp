#include<stdio.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	
	int yue,bei=m;
	while(bei%n!=0){
		bei+=m;
	}
	yue=(m*n)/bei;
	printf("%d %d",yue,bei);
	
	return 0;
}
