#include<stdio.h>
#include<math.h>
int main(void){
	
	int n5,n6,n7,n11,count;
	
	n5=n6=n7=n11=count=0;
	
	while(!(n5==1&&n6==5&&n7==4&&n11==10)){
		count++;
		n5=(n5+1)%5;
		n6=(n6+1)%6;
		n7=(n7+1)%7;
		n11=(n11+1)%11;
	}
	
	printf("%d",count);
	
	return 0;
}
