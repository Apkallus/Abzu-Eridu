#include<stdio.h>

int main(void){
	
	char*lang[]={" B"," F"," P"," J"," C"};
	char **q;
	int k;
	for(k=0;k<5;k++){
		q=&lang[k];
		printf("%s\n",*q);
	}
	return 0;
}
