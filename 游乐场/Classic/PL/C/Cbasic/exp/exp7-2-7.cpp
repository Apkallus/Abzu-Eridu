#include<stdio.h>
#include<math.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	int a[6][6],b[6][6];
	m=m%n;

	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			scanf("%d",&a[i][k]);
			if(k+m<=n-1){
				b[i][k+m]=a[i][k];
			}else{
				b[i][k+m-(n-1)-1]=a[i][k];
			}
		}
	}	
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			printf("%d ",b[i][k]);
		}
		putchar('\n');
	}
	
	return 0;
}
