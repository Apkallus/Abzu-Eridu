#include<stdio.h>
int main(void){
	
	char ch,str[80];
	int i;
	for(i=0;(ch=getchar())!='\n';i++){
		str[i]=ch;	
		if(ch>='A'&&ch<='Z'){
			putchar('Z'-ch+'A');	
		}else{
			putchar(ch);
		}
		
	}
	str[i]='\0';
	
	return 0;
}
