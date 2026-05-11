#include<stdio.h>
int *GetMax(int score[],int n);
int main(void){
	int i,score[10]={3,7,64,8,0,34,87,23,96,12},*p;
	p=GetMax(score,10);
	printf("Max:%d\n",*p);
	return 0;
}
int *GetMax(int score[],int n){
	int i,temp,pos=0;
	temp=score[0];
	for(i=0;i<n;i++){
		if(score[i]>temp){
			temp=score[i];
			pos=i;
		}
	}
	return &score[pos];
}
