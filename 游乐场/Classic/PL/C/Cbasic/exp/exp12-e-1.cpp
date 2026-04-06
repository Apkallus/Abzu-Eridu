#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main(void){
	
	FILE *fp;

	if((fp=fopen("exp12-e-1f.txt","r"))==NULL){
		printf("can not open file");
		exit(0);
	}
	char a[40],af[4]={"for"},t[4];
	while(fgets(a,40,fp)!=NULL){
		for(int i=0,end=strlen(a);i<=end-1-1-1;i++){
			int k;
			for(k=0;k<=3-1;k++){
				t[k]=a[k+i];
			}
			t[k]='\0';
			if(strcmp(af,t)==0){
				puts(a);
				break;
			}
		}
	}
	
	
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
	return 0;
}
