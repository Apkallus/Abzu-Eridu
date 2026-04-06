#include<stdio.h>
struct info{
	char name[11];
	long int birthday;
	char tel[18];
};
int main(void){
	
	int n;
	scanf("%d",&n);
	struct info res[10],temp;
	for(int i=0;i<=n-1;i++){
		scanf("%s%ld%s",res[i].name,&res[i].birthday,res[i].tel);
	}
	
	for(int i=1;i<=n-1;i++){
		for(int k=0;k<=n-1-i;k++){
			if(res[k].birthday<res[k+1].birthday){
				temp=res[k];
				res[k]=res[k+1];
				res[k+1]=temp;
			}
		}
	}
	
	for(int i=n-1;i>=0;i--){
		printf("%s %ld %s\n",res[i].name,res[i].birthday,res[i].tel);
	}
	
	return 0;
} 
