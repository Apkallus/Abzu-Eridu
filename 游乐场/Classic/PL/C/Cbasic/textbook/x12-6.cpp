#include<stdio.h>
#include<string.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp,*fp1;
	long int filestart,rowend;
	int size=sizeof(char);
	if((fp=fopen("x12-5.cpp","r"))==NULL){
		perror("open error");
		exit(0);
	}	
	if((fp1=fopen("x12-6f.txt","w"))==NULL){
		perror("open error");
		exit(0);
	}
	
	char ch;
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF&&ch!='#'){
			fputc(ch,fp1);
		}
	}
	
	if(fclose(fp)){
		perror("close error");
		exit(0);
	}
	if(fclose(fp1)){
		perror("close error");
		exit(0);
	}
	return 0;
}
