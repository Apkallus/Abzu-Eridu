#include<stdio.h>
#include<stdlib.h>
FILE *openfile(char *strp);
void fileclose(FILE *fp);

int main(void){
	
	FILE *fp1,*fp2;
	fp1=openfile("x12-3f1.txt");
	fp2=openfile("x12-3f2.txt");
	char ch1,ch2;
	int row=1,cal=0;; 
	while(!feof(fp1)&&!feof(fp2)){
		ch1=fgetc(fp1);
		ch2=fgetc(fp2);
		cal++;	
		if(ch1!=ch2){
			break;
		}else if(ch1=='\n'){
			row++;
			cal=0;
		}
	}
	printf("ch1=%c,ch2=%c,row=%d,col=%d",ch1,ch2,row,cal);
	
	fileclose(fp1);
	fileclose(fp2);
	
	return 0;
}
FILE *openfile(char *strp){
	FILE *fp;
	if((fp=fopen(strp,"r"))==NULL){
		perror("open error");
		exit(0);
	}
	return fp;
}
void fileclose(FILE *fp){
	if(fclose(fp)){
		perror("close error");
		exit(0);
	}
}

