#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	double high,sum=0;
	scanf("%lf%d",&high,&n);	
	
	if(n!=0){
		for(int i=1;i<=n;i++){
			if(i==1){
				sum=sum+high;
			}else{
				sum=sum+high*2;
			}
			high=high/2;
			
		}		
	}else{
		high=0;
	}

	printf("%.1lf %.1lf",sum,high);
	
	return 0;
}
