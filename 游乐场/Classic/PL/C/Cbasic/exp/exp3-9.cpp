#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	
	switch(n%5){
		case 1:case 2:case 3:
			printf("Fishing");break;
		case 4:case 5:
			printf("Drying");break;
	}
	printf("in day %d",n);
	
	return 0;
}
