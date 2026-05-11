#include<stdio.h>
#include<math.h>
void pblank(int n){
	for(int i=1;i<=n;i++){
		putchar(' ');
	}
}
int main(void){
	
	int n;
	scanf("%d",&n);	
	int a[10][10]={{1},{1,1}};
	for(int i=0;i<=n-1;i++){
		pblank(n-1-i);
		for(int k=0;k<=i;k++){
			if(k==0||k==i){
				a[i][k]=1;
				printf("%4d",a[i][k]);
			}else{
				a[i][k]=a[i-1][k-1]+a[i-1][k];
				printf("%4d",a[i][k]);
			}
		}
		putchar('\n');
	}
	return 0;
}
