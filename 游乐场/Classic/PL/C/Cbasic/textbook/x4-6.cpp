#include<stdio.h>
#include<stdlib.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int i,start,end;
	start=pow(10,n-1);
	end=pow(10,n)-1;
	int f,sum,item;
	for(i=start;i<=end;i++){
		sum=0;
		item=i;
		for(f=1;f<=n;f++){
			sum=sum+pow(item%10,n);
			item=item/10;
		}
		if(sum==i){
			printf("%d\n",i);
		}
	}
	
	return 0;
}



