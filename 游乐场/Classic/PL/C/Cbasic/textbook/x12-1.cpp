#include<stdio.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp;
	if((fp=fopen("e12-1f.txt","r"))==NULL){
		perror("open error");
		exit(0);
	}
	
	char ch;
	int digit,letter,other;
	digit=letter=other=0;
	while(!feof(fp)){
		ch=fgetc(fp);
		if(ch!=EOF){
			if(ch>='0'&&ch<='9'){
				digit++;
			}else if(ch>='a'&&ch<='z'||ch>='A'&&ch<='Z'){
				letter++;
			}else{
				other++;
			}
		}
	}
	printf("digit=%d,letter=%d,other=%d\n",digit,letter,other);
	
	if(fclose(fp)){
		perror("close error");
		exit(0);
	}
	return 0;
}
