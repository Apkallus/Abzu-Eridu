#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,min,num;
	scanf("%d",&n);	
	
	for(int i=1;i<=n;i++){
		scanf("%d",&num);	
		if(i==1){
			min=num;
		}else{
			if(num<min){
				min=num;
			}
		}
	}
	printf("min = %d",min);
	
	return 0;
}
