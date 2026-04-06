#include<stdio.h>
#include<stdlib.h>
long int size;
struct LogData{
	long int logid;
	char logdate[11];
	char lognote[15];
	double charge;
	double balance;
};
int inputchoice();
long int getLogcount(FILE *fp);
void ListAllLog(FILE *fp);
void QueryLastLog(FILE *fp);
FILE *openfile(char *openmode);
void closefile(FILE *fp);
void AddNewLog(FILE *fp);
void UpdateLog(FILE *fp);

int main(void){
	
	FILE *fp;
	int choice;
	size=sizeof(struct LogData);
	while((choice=inputchoice())!=0){
		switch(choice){
			case 1:						/*创建并添加记录*/
				fp=openfile("ab+");
				AddNewLog(fp);
				closefile(fp);
				break;
			case 2:						/*显示所有记录*/
				fp=openfile("rb");
				ListAllLog(fp);
				closefile(fp);
				break;
			case 3:						/*显示最后一条记录*/
				fp=openfile("rb");
				QueryLastLog(fp);
				closefile(fp);
				break;
			case 4:
				fp=openfile("rb+");
				UpdateLog(fp);
				closefile(fp);
				break;
			default:
				printf("Input Error.");
				break;
		}
		
	}

	return 0;
}

int inputchoice(){
	int mychoice;
	printf("\nEnter your choice:\n");
	printf("1-Add a new cash LOG. \n2-List All Cash LOG. \n");
	printf("3-Query Last cash LOG. \n4-Update LOG. \n0-End program. \n");
	scanf("%d",&mychoice);
	return mychoice;
}
FILE *openfile(char *openmode){
	FILE *fp;
	if((fp=fopen("t12-7fcashbox.dat",openmode))==NULL){
		perror("can not open file cashbox!\n");
		exit(0);
	}
	return (fp);
}
void closefile(FILE *fp){
	if(fclose(fp)){
		perror("Can not close the file");
		exit(0);
	} 
}
long int getLogcount(FILE *fp){
	long int begin,end,logcount;
	fseek(fp,0L,SEEK_SET);
	begin=ftell(fp);
	fseek(fp,0L,SEEK_END);
	end=ftell(fp);
	printf("--begin,end=%ld,%ld\n(end-begin)/size%ld\n",begin,end,(end-begin)/size);
	logcount=(end-begin)/size;/*示例为(end-begin)/size-1; */
	return logcount;
}

void ListAllLog(FILE *fp){
	struct LogData log;
	fseek(fp,0L,SEEK_SET);
	fread(&log,size,1,fp);
	printf("logid logdate lognote charge balance \n");
	while(!feof(fp)){
		printf("%6ld %-11s %-15s %10.2lf %10.2lf\n",
		log.logid,log.logdate,log.lognote,log.charge,log.balance);
		fread(&log,size,1,fp);
	}
}

void QueryLastLog(FILE *fp){
	struct LogData log;
	long int logcount;
	logcount=getLogcount(fp);
	if(logcount>0){
		fseek(fp,size*(logcount-1),SEEK_SET);
		fread(&log,size,1,fp);
		printf("The last log is:\n");
		printf("%6ld %-11s %-15s %10.2lf %10.2lf\n",
		log.logid,log.logdate,log.lognote,log.charge,log.balance);
		
	}else{
		printf("No logs in file!\n");
	}
}

void AddNewLog(FILE *fp){
	struct LogData log,lastlog;
	long int logcount;
	printf("Input logdate(format:2006-01-01):");
	scanf("%s",log.logdate);
	printf("Input lognote:");
	scanf("%s",log.lognote);
	printf("Input Charge:Income+ and expend-:");
	scanf("%lf",&log.charge);
	
	logcount=getLogcount(fp);
	printf("--logcount=%ld\n",logcount);
	if(logcount>0){
		fseek(fp,size*(logcount-1),SEEK_SET);
		fread(&lastlog,size,1,fp);
		log.logid=lastlog.logid+1;
		log.balance=lastlog.balance+log.charge;
	}else{
		log.logid=1;
		log.balance=log.charge;
	}
	rewind(fp); 
	/* 
	如果不移动文件指针则写入无效 
	在追加模式下新数据到末尾 */
	fwrite(&log,size,1,fp);
	printf("logid=%ld\n",log.logid);
}

void UpdateLog(FILE *fp){
	struct LogData newlog,log;
	long int logcount;
	int find=0;
	long int begin,end;
	double chazhi;

	
	logcount=getLogcount(fp);
	if(logcount==0){
		printf("No logs in file!\n");
	}else{
		printf("Input logid:");
		scanf("%ld",&newlog.logid);
		printf("Input logdate(format:2006-01-01):");
		scanf("%s",newlog.logdate);
		printf("Input lognote:");
		scanf("%s",newlog.lognote);
		printf("Input Charge:Income+ and expend-:");
		scanf("%lf",&newlog.charge);
		
		rewind(fp);
		fread(&log,size,1,fp);
		while(!feof(fp)){
			printf("log.logid=%ld,log.logdate=%s,ftell(fp)=%ld\n",log.logid,log.logdate,ftell(fp)/size);
			if(find){
				log.balance+=chazhi;
				fseek(fp,-1*size,SEEK_CUR);	
				fwrite(&log,size,1,fp);
				fseek(fp,ftell(fp),SEEK_SET);
			}
			if(log.logid==newlog.logid){	
				printf("enter ftell=%ld\n",ftell(fp)/size);
				chazhi=newlog.charge-log.charge;	
				newlog.balance=chazhi+log.balance;
				fseek(fp,-1*size,SEEK_CUR);	
				printf("-1 ftell=%ld\n",ftell(fp)/size);
				fwrite(&newlog,size,1,fp);	
				fseek(fp,ftell(fp),SEEK_SET);	
				/*
				fseek(fp,1*size,SEEK_CUR);
				fseek(fp,-1*size,SEEK_CUR);	
				fseek(fp,0L,SEEK_CUR);	
				覆盖写入fwrite后如果没有手动移位，那么下一项fread的是被覆盖的数据
				如果手动移位，那么fread的是更新后的信息 
				使用fseek移动后再回来或者移动到ftell的位置到下一项 
				猜测：新数据不是覆盖而是插入，直到更新后才把旧数据删除
				*/	
				printf("fixed_ftell=%ld\n",ftell(fp)/size);
				find=1;			
			}
			fread(&log,size,1,fp);
		}
		if(find==0){
			printf("Can not find log.\n");
		}
	}
}
