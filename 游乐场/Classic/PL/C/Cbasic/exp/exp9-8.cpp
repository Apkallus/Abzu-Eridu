#include<stdio.h>
struct info{
	char name[11];
	long int birthday;
	char tel[18];
};
int main(void){
	
	int n;
	scanf("%d",&n);
	struct info a[10],temp;
	for(int i=0;i<=n-1;i++){
		scanf("%s%ld%s",a[i].name,&a[i].birthday,a[i].tel);
	}
	for(int i=1;i<=n-1;i++){
		for(int k=0;k<=n-1-i;k++){
			if(a[k].birthday>a[k+1].birthday){
				temp=a[k];
				a[k]=a[k+1];
				a[k+1]=temp;
			}
		}
	}
	for(int i=0;i<=n-1;i++){
		printf("%s %ld %s\n",a[i].name,a[i].birthday,a[i].tel);
	}
	return 0;
}
