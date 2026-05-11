#include<stdio.h>
#include<stdlib.h>
int main(void){
	
//	FILE fp;
	FILE *fp;
	int n,num;
	
//	if((fp=fopen("error12_2f.dat","r"))==NULL){
	if((fp=fopen("error12_2f.dat","wb"))==NULL){
		printf("can not open file");
		exit(0);
	}
//	while(fscanf(fp,"%d",&n)==EOF){
	scanf("%d",&num);
	while(num!=-1){
		fwrite(&num,sizeof(int),1,fp);
		scanf("%d",&num);
	}	
	
	fclose(fp);
	
	return 0;
}
