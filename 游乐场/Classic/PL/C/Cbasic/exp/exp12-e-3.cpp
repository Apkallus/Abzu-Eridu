#include<stdio.h>
#include<string.h>
#include<stdlib.h>
struct info{
	int id;
	char name[10];
	double balance;
};
int size=sizeof(struct info);
FILE *open(char *filename,char *mod);
void close(FILE *fp);
void add(FILE *fp);
void update(FILE *fp);
void check(FILE *fp);
int main(void){
	
	FILE *fp;
	char *filename="exp12-e-3f.dat";
	int choice;
	
	do{
		printf("1.add 2.check 3.update 0.exit\n");
		scanf("%d",&choice);
		switch(choice){
			case 1:
				fp=open(filename,"ab+");
				add(fp);
				close(fp);
				break;
			case 2:
				fp=open(filename,"rb");
				check(fp);
				close(fp);
				break;
			case 3:
				fp=open(filename,"rb+");
				update(fp);
				close(fp);
				break;
			default:
				break;
		}
	}while(choice!=0);
	return 0;
}
void close(FILE *fp){
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
}
FILE *open(char *filename,char *mod){
	FILE *fp;
	if((fp=fopen(filename,mod))==NULL){
		perror("file open");
		exit(0);
	}
	return fp;
}
void add(FILE *fp){
	struct info t;
	printf("enter id,name,balance\n");
	scanf("%d%s%lf",&t.id,t.name,&t.balance);
	fwrite(&t,size,1,fp);
}
void check(FILE *fp){
	struct info t;
	int cid,flag=0;
	printf("enter id\n");
	scanf("%d",&cid);
	while(fread(&t,size,1,fp)!=0){
		if(t.id==cid){
			printf("id\tname\tbalance\n%d\t%s\t%.2lf\n",t.id,t.name,t.balance);
			flag=1;
		}
	}
	if(flag==0){
		printf("not exist\n");
	}
}
void update(FILE *fp){
	struct info t;
	int flag=0,uid;
	double trade;
	printf("enter id,trade\n");
	scanf("%d%lf",&uid,&trade);
	while(fread(&t,size,1,fp)!=0){
		if(t.id==uid){
			printf("id\tname\tbalance\n%d\t%s\t%.2lf\n",t.id,t.name,t.balance);
			t.balance+=trade;
			fseek(fp,-1*size,SEEK_CUR);
			fwrite(&t,size,1,fp);
			flag=1;
			break;
		}
	}
	if(flag==0){
		printf("not exist\n");
	}	
}
