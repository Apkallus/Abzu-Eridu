#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){
	
	char ch;
	FILE *fp;
	if((fp=fopen("exp12-b-1f.txt","r"))==NULL){
		perror("file open");
		exit(0);
	}
	
	int letter=0,digit=0,other=0;
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			if(ch>='0'&&ch<='9'){
				digit++;
			}else if(ch>='A'&&ch<='Z'||ch>='a'&&ch<='z'){
				letter++;
			}else{
				other++;
			}
		}
	}
	printf("digit=%d,letter=%d,other=%d",digit,letter,other);
	
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
	
	return 0;
}
