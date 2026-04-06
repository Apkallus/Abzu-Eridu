#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){
	
	FILE *fp;
	if((fp=fopen("exp12-b-2f.txt","w"))==NULL){
		perror("file open");
		exit(0);
	}
	
	double num;
	scanf("%lf",&num);
	while(num!=-1){
		fprintf(fp,"%lf\n",num);
		scanf("%lf",&num);		
	}
	
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
	
	return 0;
}
