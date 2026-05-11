#include<stdio.h>
#include<stdlib.h>
#include<string.h>
FILE *openfile(char *strp);
void fileclose(FILE *fp);

int main(void){
	
	FILE *fp;
	char tailname[5];
	char filename[10]="x12-2f";
	double num;
	int count=1;
	scanf("%lf",&num);
	while(num!=-1){
		itoa(count,tailname,10);
		strcat(filename,tailname);strcat(filename,".txt");
		fp=openfile(filename);
		fprintf(fp,"%lf",num);
		fclose(fp);
		strcpy(filename,"x12-2f");
		count++;
		scanf("%lf",&num);
	}
	
	return 0;
}
FILE *openfile(char *strp){
	FILE *fp;
	if((fp=fopen(strp,"w"))==NULL){
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

