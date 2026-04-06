#include<stdio.h>
#include<math.h>
int main(void){
	
	char str[80];
	char ch;
	int i;
	for(i=0;(ch=getchar())!='\n';i++){
		str[i]=ch;
	}
	str[i]='\0';
	for(int k=0;k<=(i-1)/2;k++){
		char temp=str[k];
		str[k]=str[i-1-k];
		str[i-1-k]=temp;
	}
	for(int k=0;k<=i-1;k++){
		putchar(str[k]);
	}
	
	return 0;
}
