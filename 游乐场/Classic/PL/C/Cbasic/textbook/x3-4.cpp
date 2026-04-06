#include<stdio.h>
int main(void)
{
	int sc,tr,n,i,a,b,c,d,e;
	scanf("%d",&n);
	
	a=b=c=d=e=0;
	for(i=1;i<=n;i++){
		scanf("%d",&sc);
		if(sc>=90){
			a++;
		}else if(sc<90&&sc>=80){
			b++;
		}else if(sc<80&&sc>=70){
			c++;
		}else if(sc<70&&sc>=60){
			d++;
		}else{
			e++;
		}
	}

	
	printf("%d %d %d %d %d",a,b,c,d,e);
	
	return 0;
}
