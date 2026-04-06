#include<stdio.h>
#include<math.h>
int main(void){
	
	char chf,ch,str[80];
	chf=getchar();
	getchar();
	int i;
	for(i=0;(ch=getchar())!='\n';i++){
		str[i]=ch;
	}
	str[i]='\0';
	int flag=0;
	for(int k=i-1;k>=0;k--){
		if(str[k]==chf){
			printf("index = %d",k);
			flag=1;
			break;
		}
	}
	if(flag==0){
		printf("Not Found");
	}
	return 0;
}
