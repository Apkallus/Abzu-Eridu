#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,a[10];
	scanf("%d",&n);	
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
	}
	int res;
	for(int i=0;i<=n-1-1;i++){
		res=a[i+1]-a[i];
		if(i%3==0){
			if(i!=0&&i%3==0){
				putchar('\n');
			}
			printf("%d",res);
		}else{
			printf(" %d",res);
		}

	}
	
	return 0;
}
