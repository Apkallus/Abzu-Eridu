#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	
	char ch='A';
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			if(k<=n-1-i){
				printf("%c ",ch);
				ch++;
			}
		}
		putchar('\n');
	}
	
	return 0;
}


