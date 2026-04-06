#include<stdio.h>
#include<string.h>
#include<stdlib.h>
struct info{
	char id[8];
	char name[20];
	int math;
	int chinese;
	int english;
	int total;
	double avg;
};

void input();
void print();

int main(void){
	
	int choice;
	printf("1.input 2.print\n");	
	scanf("%d",&choice);
	
	switch(choice){
		case 1:
			input();
			break;
		case 2:
			print();
			break;
		default:
			break;
	}


	return 0;
}

void input(){
	FILE *fp;
	if((fp=fopen("exp12-b-3f.txt","w"))==NULL){
		perror("open file");
		exit(0);
	}
	
	struct info stud;
	scanf("%s",stud.id);
	while(stud.id[0]!='#'){
		scanf("%s%d%d%d",stud.name,&stud.math,&stud.chinese,&stud.english);
		stud.total=stud.math+stud.chinese+stud.english;
		stud.avg=stud.total/3.0;
		fprintf(fp,"%s %s %d %d %d %d %.0lf\n",
			stud.id,stud.name,stud.math,stud.chinese,stud.english,stud.total,stud.avg);
		scanf("%s",stud.id);
	}
	
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}
}

void print(){
	FILE *fp;
	if((fp=fopen("exp12-b-3f.txt","r"))==NULL){
		perror("open file");
		exit(0);
	}	
	struct info stud;
	char ch;
	fscanf(fp,"%s %s %d %d %d %d %lf",
		stud.id,stud.name,&stud.math,&stud.chinese,&stud.english,&stud.total,&stud.avg);

	while(!feof(fp)){
		printf("%s %s %d %d %d %d %.0lf\n",
			stud.id,stud.name,stud.math,stud.chinese,stud.english,stud.total,stud.avg);		
		fscanf(fp,"%s %s %d %d %d %d %lf",
			stud.id,stud.name,&stud.math,&stud.chinese,&stud.english,&stud.total,&stud.avg);
	}
	if(fclose(fp)){
		perror("file close");
		exit(0);
	}	
}
