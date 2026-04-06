#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h>
int main(void){
	
	int n,*p;
	scanf("%d",&n);
	
	if((p=(int*)malloc(sizeof(int)*n))==NULL){
		perror("malloc error");
		exit(1);
	}
	
	
	for(int i=0;i<=n-1;i++){
		scanf("%d",&p[i]);
	}
	double sum=0,max,min;
	for(int i=0;i<=n-1;i++){
		if(i==0){
			max=min=p[i];
		}else{
			if(max<p[i]){
				max=p[i];
			}
			if(min>p[i]){
				min=p[i];
			}
		}
		sum+=p[i];
	}
	printf("average = %.2lf\nmax = %.2lf\nmin = %.2lf",sum/n,max,min);
	free(p);//使用后释放 
	
	return 0;
}
