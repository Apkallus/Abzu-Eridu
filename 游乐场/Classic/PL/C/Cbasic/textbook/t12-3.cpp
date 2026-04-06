#include <stdio.h>
#include <string.h>
#include <stdlib.h>
struct stdu{
	char username[20];
	char password[8];
};

int main(void){
	
	FILE *fp1,*fp2;
	int i;
	struct stdu su;
	char ch;
	
	if((fp1=fopen("t12-2f.txt","r"))==NULL){
		perror("File open error!");
		exit(0);
	}
	if((fp2=fopen("t12-3f.txt","w"))==NULL){
		perror("File open error!");
		exit(0);
	}	
	while(!feof(fp1)){
		ch=fgetc(fp1);
		if(ch!=EOF){
			fputc(ch,fp2);
		}
	}
	
	if(fclose(fp1)){
		perror("Can not close the file!");
		exit(0);
	}
	if(fclose(fp2)){
		perror("Can not close the file!");
		exit(0);
	}
	
	
	if((fp2=fopen("t12-3f.txt","r"))==NULL){
		perror("File open error!");
		exit(0);
	}
	
	int count=0;	
	while(!feof(fp2)){
		ch=fgetc(fp2);
		if(ch!=EOF){
			count++;
		}
	}
	printf("count = %d\n",count);
	if(fclose(fp2)){
		perror("Can not close the file!");
		exit(0);
	}
	return 0;
}
