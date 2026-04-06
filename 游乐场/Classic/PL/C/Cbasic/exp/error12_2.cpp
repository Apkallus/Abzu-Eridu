#include<stdio.h>
#include<stdlib.h>
int main(void){
	
//	FILE fp;
	FILE *fp;
	int n,sum;
	
//	if((fp=fopen("error12_2f.dat","r"))==NULL){
	if((fp=fopen("error12_2f.dat","ab+"))==NULL){
		printf("can not open file");
		exit(0);
	}
	sum=0;
//	while(fscanf(fp,"%d",&n)==EOF){
	while(fread(&n,sizeof(int),1,fp)!=0){
		printf("n=%d ",n);
		sum=sum+n;
	}	
	rewind(fp);
//	fprintf(fp," %d",sum);	
	fwrite(&sum,sizeof(int),1,fp);
	fclose(fp);
	
	return 0;
}
