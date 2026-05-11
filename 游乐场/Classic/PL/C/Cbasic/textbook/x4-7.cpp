#include<stdio.h>
int main(void){
	
	int m,n;
	scanf("%d%d",&m,&n);
	
	int max,min;
	if(m>n){
		max=m;
		min=n;
	}else{
		max=n;
		min=m;
	}
	
	int beishu=max,count=1;
	while(beishu%min!=0){
		beishu=max*count;
		count++;
	}
	
	int yueshu,i;
	for(i=1;i<=min;i++){
		if(min%i==0&&max%i==0){
			yueshu=i;
		}
	}
	printf("%d %d",yueshu,beishu);
	
	return 0;
}
