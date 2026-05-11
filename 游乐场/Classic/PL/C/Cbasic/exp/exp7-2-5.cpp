#include<stdio.h>
#include<math.h>
int main(void){
	
	int t;
	scanf("%d",&t);	
	for(int ti=1;ti<=t;ti++){
		int n,flag=1;
		scanf("%d",&n);
		for(int i=0;i<=n-1;i++){
			for(int k=0;k<=n-1;k++){
				int num;
				scanf("%d",&num);
				if(i>k&&num!=0){
					flag=0;
				}	
			}
		}
		if(flag){
			printf("YES\n");
		}else{
			printf("NO\n");
		}
	}
	
	return 0;
}
