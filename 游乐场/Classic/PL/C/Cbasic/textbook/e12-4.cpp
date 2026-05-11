#include <stdio.h>
#include <string.h>
#include <stdlib.h>
struct stdu{
	char username[20];
	char password[8];
};
void encrypt(char *pwd);
int checkUserValid(struct stdu *psu);
int main(void){
	
	struct stdu su;
	printf("Enter sysuser(name password):");
	scanf("%s%s",su.username,su.password);
	if(checkUserValid(&su)==1){
		printf("Valid user!\n");
	}else{
		printf("Invalid user!\n");
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
int checkUserValid(struct stdu *psu){
	FILE *fp;
	char usr[30],usr1[30],pwd[10];
	int check=0;
	
	strcpy(usr,psu->username);
	strcpy(pwd,psu->password);
	encrypt(pwd);
	strcat(usr," "); strcat(usr,pwd); strcat(usr,"\n");
	
	if((fp=fopen("t12-2f.txt","r"))==NULL){
		perror("File open error!");
		exit(0);
	}
	
	while(!feof(fp)){
		fgets(usr1,30,fp);
		if(strcmp(usr,usr1)==0){
			check=1;
			break;
		}
	}
	
	if(ferror(fp)){
		perror("file r/w error");
	}else if(feof(fp)){
		printf("EOF success\n");
	}
	if(fclose(fp)){
		perror("Can not close the file!");
		exit(0);
	}
	return check;
}
