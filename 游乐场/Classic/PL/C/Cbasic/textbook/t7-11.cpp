#include<stdio.h>
int main(void){
	
	char str[80];
	
	int i;
	for(i=0;(str[i]=getchar())!='\n';i++){
	}
	str[i]='\0';
	
	int resi=0;
	char res[80];
	for(int y=i-1;y>=0;y--){
		res[resi]=str[y];
		resi++;
	}
	res[resi]='\0';
	
	for(int k=0;res[k]!='\0';k++){
		putchar(res[k]);
	}
	
	return 0;
}
