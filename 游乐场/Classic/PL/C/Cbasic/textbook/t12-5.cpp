#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp;
	char ch;
	
	if((fp=fopen("t12-5f.txt","w+"))==NULL){
		perror("error");
		exit(0);
	}
	
	while((ch=getchar())!='\n'){
		fputc(ch,fp);
	}
		
	rewind(fp);
	putchar('\n');
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			putchar(ch);
		}		
	}
	
	
	if(fclose(fp)){
		perror("error");
		exit(0);
	}
	return 0;
}
