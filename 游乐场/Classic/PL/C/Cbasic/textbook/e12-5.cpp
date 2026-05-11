#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define SIZE 5
struct stdu{
	char username[20];
	char password[8];
};
void encrypt(char *pwd);
int main(void){
	
	FILE *fp;
	int i;
	struct stdu u[SIZE],su[SIZE],*pu=u,*psu=su;
	
	if((fp=fopen("t12-5f.txt","wb+"))==NULL){
		perror("File open error!");
		exit(0);
	}
	
	for(i=1;i<=SIZE;i++,pu++){
		printf("Enter %d th sysuser(name password):",i);
		scanf("%s%s",pu->username,pu->password);
		encrypt(pu->password);
	}
	pu=u;
	fwrite(pu,sizeof(struct stdu),SIZE,fp);
	rewind(fp);
	fread(psu,sizeof(struct stdu),SIZE,fp);
	
	for(i=0;i<=SIZE-1;i++,psu++){
		printf("%-10s%s\n",psu->username,psu->password);
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
