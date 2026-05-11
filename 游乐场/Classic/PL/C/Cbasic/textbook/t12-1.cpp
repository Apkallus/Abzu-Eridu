#include <stdio.h>
#include <stdlib.h>
struct stdu{
	long int num;
	char name[20];
	int score;
};
int main(void){
	
	FILE *fp;
/*	long num;
	char stname[20];*/
	int i,score;
	int avg_score=0;
	struct stdu st,stmax,stmin;
	
	if((fp=fopen("E:/App/Dev-Cpp/C_program/e12-1f.txt","r"))==NULL){/* 示例的\\报错 替换为/ */
		perror("File open error!");
		exit(0);
	}
	
	for(i=0;i<=5-1;i++){
		fscanf(fp,"%ld%s%d",&st.num,st.name,&st.score);
		avg_score+=st.score;
		printf("%ld %s %d\n",st.num,st.name,st.score);
		if(i==0){
			stmax=stmin=st;
		}else{
			if(st.score>stmax.score){
				stmax=st;
			}else if(st.score<stmin.score){
				stmin=st;
			}
		}
	}
	printf("Average score:%d\n",avg_score/5);
	printf("Max score:%ld %s %d\n",stmax.num,stmax.name,stmax.score);
	printf("Min score:%ld %s %d\n",stmin.num,stmin.name,stmin.score);
	if(fclose(fp)){
		perror("Can not close the file!");
		exit(0);
	}
	
	return 0;
}
