#include<stdio.h>
struct info{
	char id[6];
	char name[10];
	int a;
	int b;
	int c;
	int total;
};
int main(void){
	
	int n;
	scanf("%d",&n);
	struct info max,temp;
	for(int i=0;i<=n-1;i++){
		scanf("%s%s%d%d%d",temp.id,temp.name,&temp.a,&temp.b,&temp.c);
		temp.total=temp.a+temp.b+temp.c;
		if(i==0){
			max=temp;
		}else{
			if(temp.total>max.total){
				max=temp;
			}
		}
	}
	printf("%s %s %d",max.name,max.id,max.total);
	return 0;
}
