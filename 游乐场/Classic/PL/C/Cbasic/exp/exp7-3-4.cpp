#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
	
	char str[80],ch;
	int i=0;
	while((ch=getchar())!='\n'){
		if(ch>='A'&&ch<='Z'){
			str[i]='Z'-ch+'A';
		}else{
			str[i]=ch;
		}
		
		i++;
	}
	str[i]='\0';
	puts(str);
	return 0;
}
