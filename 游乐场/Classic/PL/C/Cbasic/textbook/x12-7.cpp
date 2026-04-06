#include<stdio.h>
#include<stdlib.h>
#define Filename "x12-7f.dat"
struct AccountData{
	long int AcctNo;
	char AcctName[15];
	double balance;
};
int size=sizeof(struct AccountData);
void update(FILE* fp);
void check(FILE* fp);
void adddata(FILE* fp);
int accountcount(FILE *fp);
int accountcount(FILE *fp);
void closefile(FILE* fp);
FILE *openfile(char *openmode);
int inputchoice();

int main(void){
	
	FILE *fp;
	int choice;
	while((choice=inputchoice())!=0){
		switch(choice){
			case 1:
				fp=openfile("ab+");
				adddata(fp);
				closefile(fp);
				break;
			case 2:
				fp=openfile("rb");
				check(fp);
				closefile(fp);
				break;
			case 3:
				fp=openfile("rb+");
				update(fp);
				closefile(fp);
				break;
			default:
				printf("\nenter choice\n");
				break;
		}
	}	
	
	return 0;
}
int inputchoice(){
	int choice;
	printf("\n1.add\n2.check\n3.update\n0.exit\n");
	scanf("%d",&choice);
	return choice;
}
FILE *openfile(char *openmode){
	FILE *fp;
	if((fp=fopen(Filename,openmode))==NULL){
		perror("open error");
		exit(0);
	}
	return fp;
}
void closefile(FILE* fp){
	if(fclose(fp)){
		perror("close error");
		exit(0);
	}
}
int accountcount(FILE *fp){
	int count=0;
	long int start,end;
	fseek(fp,0L,SEEK_SET);
	start=ftell(fp);
	fseek(fp,0L,SEEK_END);
	end=ftell(fp);
	count=(end-start)/size;
	return count;
}
void adddata(FILE* fp){
	struct AccountData data,lastdata;
	printf("\nenter accname:");
	scanf("%s",data.AcctName);
	printf("\nenter balance:");
	scanf("%lf",&data.balance);
	
	int count=accountcount(fp);
	if(count==0){
		data.AcctNo=1;
	}else{
		fseek(fp,(count-1)*size,SEEK_SET);
		fread(&lastdata,size,1,fp);
		data.AcctNo=lastdata.AcctNo+1;
	}
	rewind(fp);
	fwrite(&data,size,1,fp);
}
void check(FILE* fp){
	struct AccountData data;
	int acctno,find=0;
	printf("\nenter acctno:");
	scanf("%d",&acctno);
	rewind(fp);
	fread(&data,size,1,fp);
	while(!feof(fp)){		
		if(acctno==data.AcctNo){
			printf("\nacctname:%s balance:%.2f",data.AcctName,data.balance);
			find=1;
			break;
		}
		fread(&data,size,1,fp);
	}
	if(find==0){
		printf("account not exist\n");
	}
}
void update(FILE* fp){
	struct AccountData data;
	int acctno,find=0;
	printf("\nenter acctno:");
	scanf("%d",&acctno);
	rewind(fp);
	fread(&data,size,1,fp);
	while(!feof(fp)){		
		if(acctno==data.AcctNo){
			printf("\nacctname:%s balance:%.2f",data.AcctName,data.balance);
			printf("\nenter newbalnce");
			scanf("%lf",&data.balance);
			fseek(fp,-size,SEEK_CUR);
			fwrite(&data,size,1,fp);
			find=1;
			break;
		}
		fread(&data,size,1,fp);
	}
	if(find==0){
		printf("account not exist\n");
	}
}
