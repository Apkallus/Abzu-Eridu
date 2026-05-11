#include<stdio.h>
#include<string.h>
int main(void){
	int i;
	char str[80],min[80];
	
	printf("input 5 str:\n");
	scanf("%s",str);
//	min=str;
	strcpy(min,str);
	for(i=1;i<5;i++){
		scanf("%s",str);
//		if(min>str){
//			min=str;
		if(strcmp(min,str)>0){
			strcpy(min,str);			
		}
	}
	printf("Min is:%s",min);
	return 0;
}
