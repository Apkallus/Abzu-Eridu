#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	int n;
	float *p;
	scanf("%d",&n);
	if((p=(float *)calloc(n,sizeof(float)))==NULL){
		printf("allocate memory faile.\n");
		exit(1);		
	}
	
	float sum=0;
	int maxi=0,mini=0;
	for(int i=0;i<=n-1;i++){
		scanf("%f",&p[i]);
		sum+=p[i];
		if(p[i]>p[maxi]){
			maxi=i;
		}else if(p[i]<p[mini]){
			mini=i;
		}
	}
	printf("average = %.2f\nmax = %.2f\nmin = %.2f",sum/n,p[maxi],p[mini]);
	
	free(p);
	return 0;
}
