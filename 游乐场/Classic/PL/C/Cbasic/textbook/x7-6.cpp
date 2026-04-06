#include<stdio.h>
int main(void){
	
	char str[80];
	int i;
	char ch;
	int count=0;
	for(i=0;(ch=getchar())!='\n';i++){
		if(ch>='A'&&ch<='Z'&&ch!='A'&&ch!='E'&&ch!='I'&&ch!='O'&&ch!='U'){
			count++;
		}
	}
	str[i]='\0';
	
	printf("%d",count);
	return 0;
}
