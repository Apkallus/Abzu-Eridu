#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
		
	char str[80],ch;
	int i=0;

	while((ch=getchar())!='#'){
		str[i]=ch;
		if(ch>='a'&&ch<='z'){
			str[i]=ch-'a'+'A';
		}else if(ch>='A'&&ch<='Z'){
			str[i]=ch-'A'+'a';
		}else{
			str[i]=ch;
		}
		i++;
	}
	str[i]='\0';
	puts(str);
	return 0;
}
