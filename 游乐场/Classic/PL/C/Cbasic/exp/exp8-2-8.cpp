#include<stdio.h>
#include<string.h>
int main(void){
	
	int n=5;
	char a[5][80],max[80];
	
	for(int i=0;i<=n-1;i++){
		scanf("%s",a[i]);
	}
	
	for(int i=1;i<=n-1;i++){
		for(int k=0;k<=n-1-i;k++){
			if(strcmp(a[k],a[k+1])>0){
				char temp[80];
				strcpy(temp,a[k]);
				strcpy(a[k],a[k+1]);
				strcpy(a[k+1],temp);
			}
		}
	}
	printf("After sorted:\n");
	for(int i=0;i<=n-1;i++){
		printf("%s\n",a+i);
	}
	
	return 0;
}
