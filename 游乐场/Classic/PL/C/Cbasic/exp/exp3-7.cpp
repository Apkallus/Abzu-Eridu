#include<stdio.h>
#include<math.h>
int main(void){
	
	int n,a=0,b=0,c=0,d=0,e=0,score;
	scanf("%d",&n);	
	for(int i=1;i<=n;i++){
		scanf("%d",&score);
		if(score>=90){
			a++;
		}else if(score>=80){
			b++;
		}else if(score>=70){
			c++;
		}else if(score>=60){
			d++;
		}else{
			e++;
		}
	}
	printf("%d %d %d %d %d",a,b,c,d,e);
	return 0;
}
