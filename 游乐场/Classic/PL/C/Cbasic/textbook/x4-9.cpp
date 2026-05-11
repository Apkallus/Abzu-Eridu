#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	
	int middle;
	middle=n/2+1;
	
	int i,star,blank,a,b,c;
	for(i=1;i<=n;i++){/*n行循环*/ 
		
		if(i<=middle){
			star=i*2-1;/*计算star的数量*/
		}else{
			star=(middle-i+middle)*2-1;
		}
		
		blank=(n-star)/2;/*计算blank的数量*/ 
		
		for(a=1;a<=blank;a++){
			printf("  ");
		}
		
		for(b=1;b<=star;b++){
			printf("* ");
		}
	
		
		if(i<n){
			printf("\n");
		}		
		
	}
	
	return 0;
}


