#include<stdio.h>
#include<stdlib.h>
void bubble(int a[],int n);
int main(void){
	
	int n,*p;
	scanf("%d",&n);
	if((p=(int *)calloc(n,sizeof(int)))==NULL){
		printf("allocate memory faile.\n");
		exit(1);
	}
	
	for(int i=0;i<=n-1;i++){
		scanf("%d",p+i);
	}

	bubble(p,n);
	
	for(int i=0;i<=n-1;i++){
		printf("%d ",p[i]);
	}
	
	free(p);
	return 0;
}

void bubble(int a[],int n){
	for(int i=1;i<=n-1;i++){
		for(int y=0;y<=n-1-i;y++){
			if(a[y]>a[y+1]){
				a[y]^=a[y+1]^=a[y]^=a[y+1];
			}
		}
	}
}
