#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
		
	char str[80],ch;
	int i=0,flag=0;
	long int num=0;

	while((ch=getchar())!='\n'){
		str[i]=ch;
		i++;
		if(ch>='0'&&ch<='9'){
			num=num*10+ch-'0';
		}
	}
	str[i]='\0';
	printf("%d",num);
	return 0;
}
