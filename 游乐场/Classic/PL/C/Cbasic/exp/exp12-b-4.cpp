#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){
	
	FILE *fp1,*fp2;
	if((fp1=fopen("exp12-b-4f1.txt","r"))==NULL){
		perror("f1 open");
		exit(0);
	}
	if((fp2=fopen("exp12-b-4f2.txt","r"))==NULL){
		perror("f2 open");
		exit(0);
	}
	
	char ch1,ch2,ch;
	int row=1,cal=1;
	while(!feof(fp1)&&!feof(fp2)){
		ch1=fgetc(fp1);
		ch2=fgetc(fp2);	
		if(ch1!=EOF&&ch2!=EOF){
			if(ch1!=ch2){
				break;	
			}else{
				if(ch1=='\n'){
					row++;
					cal=1;
				}else{
					cal++;
				}
			}
		}		
	}
	if(ch1==ch2&&ch1==EOF){
		printf("same\n");
	}else{
		printf("%c,%c\nrow=%d,cal=%d\n",ch1,ch2,row,cal);
	}
	
	if(fclose(fp1)){
		perror("f1 close");
		exit(0);
	}
	if(fclose(fp2)){
		perror("f1 close");
		exit(0);
	}	
	return 0;
}
