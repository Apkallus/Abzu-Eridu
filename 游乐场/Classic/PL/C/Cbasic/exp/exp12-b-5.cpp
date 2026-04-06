#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){

	FILE *fp;
	if((fp=fopen("exp12-b-4f1.txt","r"))==NULL){
		perror("file open");
		exit(0);
	}
	
	char ch;
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			putchar(ch);	
		}
	}
	putchar('\n');
	
	int count=1;
	rewind(fp);
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			if(ch=='\n'){
				putchar(ch);
				count++;
			}else{
				putchar(ch-'a'+'A');
			}
				
		}
	}
	putchar('\n');	
	printf("count=%d",count);
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
	return 0;
}
