#include<stdio.h>
#include<math.h>
int main(void){
	
	char str[80],ch;
	int i=0,count=0;
	while((ch=getchar())!='\n'){
		str[i]=ch;
		i++;
		if(ch>='A'&&ch<='Z'&&ch!='A'&&ch!='E'&&ch!='I'&&ch!='O'&&ch!='U'){
			count++;
		}
	}
	str[i]='\0';
	printf("%d",count);
		
	return 0;
}
