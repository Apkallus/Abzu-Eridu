#include<stdio.h>
#include<stdlib.h>
int main(void){
	char ch;
//	FILE fp;
	FILE *fp;
	
//	if((fp=fopen("a.txt","w"))!=NULL){
	if((fp=fopen("errpr12_1f.txt","w"))==NULL){
		printf("Can not open file");
		exit(0);
	}
	while((ch=getchar())!='\n'){
		fputc(ch,fp);
	}
	return 0;
}
