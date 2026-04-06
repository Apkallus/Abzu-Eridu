#include<stdio.h>
#include<math.h>
int main(void){
	
	int yy,mm,dd;
	scanf("%d/%d/%d",&yy,&mm,&dd);	
	
	int is=0;
	if(yy%4==0&&yy%100!=0||yy%400==0){
		is=1;
	}
	int sum=dd;
	for(int i=1;i<=mm-1;i++){
		switch(i){
			case 1:case 3:case 5:case 7:case 8:case 10:case 12:
				sum+=31;
				break;
			case 2:
				sum+=28;
				if(is){
					sum+=1;
				}
				break;
			default:
				sum+=30;
				break;
		}
	}
	printf("%d",sum);
	return 0;
}
