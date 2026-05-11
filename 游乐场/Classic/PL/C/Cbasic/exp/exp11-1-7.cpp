#include<stdio.h>
#include<string.h>
#define han_utf8 3
int main(void){
	
	char str[7*han_utf8+1],res[4*han_utf8+1];
	for(int i=0;i<=4-1;i++){
		gets(str);
		for(int k=0;k<=3-1;k++){
			res[i*han_utf8+k]=str[k];
		}
	}
	res[4*han_utf8]='\0';
	puts(res);
	
	return 0;
}
