#include<stdio.h>
int main(void){
	
	int m,n,j,k;
	
	do{
		printf("Input m:");
		scanf("%d",&m);
		printf("Input n:");
		scanf("%d",&n);
	}while(m<0||n<0);
	
	j=m;
//	while(j/n!=0){
	while(j%n!=0){
		j=j+m;
	}
	
	k=(m*n)/j;
	printf("最大公约数%d\n最小公倍数%d\n",k,j);
	
	
	return 0;
}
