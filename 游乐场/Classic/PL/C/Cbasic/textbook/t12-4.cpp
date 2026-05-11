#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp;
	char ch;
	int count=0;
	
	if((fp=fopen("t12-4f.txt","r"))==NULL){
		perror("error");
		exit(0);
	}
	
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			if(ch=='\n'){
				count++;
			}
			putchar(ch);			
		}
	}
	
	rewind(fp);
	printf("\n\ncount=%d\nafter translate:\n",count);
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			if(ch>='A'&&ch<='Z'){
				putchar(ch-'A'+'a');
			}else{
				putchar(ch);
			}
		}
	}
	
	
	if(fclose(fp)){
		perror("error");
		exit(0);
	}
	return 0;
}
