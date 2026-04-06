#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp;
	long int size=sizeof(long int),num,sum=0;
	if((fp=fopen("x12-4.dat","ab+"))==NULL){
		perror("open error");
		exit(0);
	}
	
	fread(&num,size,1,fp);
	while(!feof(fp)){
		printf("%ld\n",num);
		sum+=num;
		fread(&num,size,1,fp);
	}
	rewind(fp);
	fwrite(&sum,size,1,fp);
	
	rewind(fp);
	fread(&num,size,1,fp);
	while(!feof(fp)){
		printf("%ld\n",num);
		fread(&num,size,1,fp);
	}
	
	if(fclose(fp)){
		perror("close error");
		exit(0);
	}
	return 0;
}

