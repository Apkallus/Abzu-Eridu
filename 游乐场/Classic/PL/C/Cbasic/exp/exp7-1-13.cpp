#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
	
	int n,a[1000],s,count=0;
	scanf("%d",&n);	
	memset(a,0,sizeof(a));
	for(int i=1;i<=n;i++){
		scanf("%d",&s);
		if(count==0){
			count++;
			a[0]=s;
			printf("%d %d",s,0+1);
		}else{
			for(int k=0;k<=count-1;k++){
				if(a[k]+s<=100){
					a[k]+=s;
					printf("\n%d %d",s,k+1);
					break;
				}else if(k==count-1){
					count++;	
				}
				
			}
		}
	}
	printf("\n%d",count);
	return 0;
}
