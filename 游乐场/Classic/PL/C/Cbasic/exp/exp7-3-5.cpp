#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
	
	char str[80],ch;
	int i=0,a[24],flag=0;
	memset(a,0,sizeof(a));
	while((ch=getchar())!='\n'){
		str[i]=ch;
		i++;
		if(ch>='A'&&ch<='Z'){
			int index=ch-'A';
			if(a[index]==0){
				putchar(ch);
				a[index]=1;
				flag=1;
			}
		}
	}
	str[i]='\0';
	if(flag==0){
		printf("Not Found");
	}
	return 0;
}
