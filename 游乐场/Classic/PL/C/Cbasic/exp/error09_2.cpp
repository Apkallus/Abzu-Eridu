#include<stdio.h>
#include<math.h>
#include<string.h>

int main(void){
	struct students{
		int number;
		char name[20];
		int score[3];
		int sum;
	};	
	int i,j,k,n,max=0;
	struct students student[10];
	printf("n=");
	scanf("%d",&n);
	for(i=0;i<n;i++){
		scanf("%d%s",&student[i].number,student[i].name);
		student[i].sum=0;
		for(j=0;j<3;j++){
			scanf("%d",&student[i].score[j]);
			student[i].sum+=student[i].score[j];
		}
	}
	
	k=0;
	max=student[0].sum;
	for(i=1;i<n;i++){
		if(max<student[i].sum){
			k=i;
			max=student[i].sum;
		}
	}
	printf("max:%s,%d\n",student[k].name,student[k].sum);
	return 0;
	
	
	return 0;
}
