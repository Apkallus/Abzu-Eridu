#include <stdio.h>
#include <string.h>
#include <stdlib.h>
struct stdu{
	char username[20];
	char password[8];
};
void encrypt(char *pwd);
int main(void){
	
	FILE *fp;
	int i;
	struct stdu su;
	
	if((fp=fopen("t12-2f.txt","w"))==NULL){
		perror("File open error!");
		exit(0);
	}
	
	for(i=1;i<=5;i++){
		printf("Enter %d th sysuser(name password):",i);
		scanf("%s%s",su.username,su.password);
		encrypt(su.password);
		fprintf(fp,"%s %s\n",su.username,su.password);
	}

	if(fclose(fp)){
		perror("Can not close the file!");
		exit(0);
	}
	
	return 0;
}
void encrypt(char *pwd){
	int i;
	for(i=0;i<=strlen(pwd)-1;i++){
	/*	pwd[i]=pwd[i]^15;*/
		if(pwd[i]=='z'){
			pwd[i]='a';
		} else{
			pwd[i]+=1;
		}
	}
}
