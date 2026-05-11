#include<stdio.h>
#include<string.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	char a[80],min[80];
	
	for(int i=1;i<=n;i++){
		scanf("%s",a);
		if(i==1){
			strcpy(min,a);
		}else{
			if(strcmp(min,a)>0){
				strcpy(min,a);
			}
		}
	}
	printf("Min is: %s",min);
	
	return 0;
}
