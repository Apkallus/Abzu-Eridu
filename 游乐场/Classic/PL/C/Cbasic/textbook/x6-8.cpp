#include<stdio.h>
int main(void){
	
	char ch,state='\0';
	int count=0;
	while((ch=getchar())!='\n'){
		if(ch==' '){
			if(state!='b'&&state!='\0'){
				count++;
			}
			state='b';
		}else{
			state='l';
		}
	}
	if(state!='b'&&state!='\0'){
		count++;
	}
	printf("%d",count);
	return 0;
}

