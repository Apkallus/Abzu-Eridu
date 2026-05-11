#include<stdio.h>
int main(void){
	
	char ch;
	ch=getchar();
	
	getchar();
	char str[80];
	int i,index=0,flag=0;
	for(i=0;(str[i]=getchar())!='\n';i++){
		if(str[i]==ch){
			flag=1;
			index=i;
		}
	}
	str[i]='\0';

	if(flag){
		printf("index = %d",index);
	}else{
		printf("Not Found");
	}
	
	return 0;
}
