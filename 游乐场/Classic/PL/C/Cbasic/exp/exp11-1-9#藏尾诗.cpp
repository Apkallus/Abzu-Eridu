#include<stdio.h>
#include<string.h>
#define han_utf8 3
int main(void){
	
	char str[9*han_utf8+1],res[4*han_utf8+1];
	for(int i=0;i<=4-1;i++){
		gets(str);
		for(int k=strlen(str)-1,count=han_utf8-1;k>=(int)strlen(str)-1-(han_utf8-1);k--,count--){
			//strlen()返回无符号，有符号的k与无符号数关系运算时，k转换为无符号，k=0-1成为最大数，从而导致无限循环 
			res[i*han_utf8+count]=str[k];
		}
	}
	res[4*han_utf8]='\0';
	puts(res);
	
	return 0;
}
