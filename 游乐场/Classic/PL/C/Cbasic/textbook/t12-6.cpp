#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp1,*fp2;
	double num,sheru;
	
	if((fp1=fopen("t12-6f1.txt","r"))==NULL){
		perror("error");
		exit(0);
	}	
	if((fp2=fopen("t12-6f2.txt","w"))==NULL){
		perror("error");
		exit(0);
	}
	
		
	while(!feof(fp1)){
		fscanf(fp1,"%lf",&num);
		printf("%f\n",num);
		if(num>=0){
			sheru=0.5;
		}else{
			sheru=-0.5;
		}
		fprintf(fp2,"%lf\n",(double)(long int)(num+sheru));
		printf("%f\n",(double)(long int)(num+sheru));	
	}
	
	
	if(fclose(fp1)){
		perror("error");
		exit(0);
	}	
	if(fclose(fp2)){
		perror("error");
		exit(0);
	}
	return 0;
}
