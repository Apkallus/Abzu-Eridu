#include<stdio.h>
#include<math.h>
#include<string.h>
struct info{
	char id[6];
	char name[10];
	int score;
};
int main(void){
	int n;
	scanf("%d",&n);
	
	double sum=0,avg;
	struct info res[10];
	for(int i=0;i<=n-1;i++){
		scanf("%s%s%d",res[i].id,res[i].name,&res[i].score);
		sum+=res[i].score;
	}	
	avg=sum/n;
	printf("%.2lf\n",avg);
	for(int i=0;i<=n-1;i++){
		if(res[i].score<avg){
			printf("%s %s\n",res[i].name,res[i].id);
		}
	}	
	return 0;
}
