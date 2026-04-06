#include<stdio.h>
int main(void){
	
	char ch;
	long int res=0;
	int firstn=1,flag=0,rf=1;
	while ((ch=getchar())!='#'){
		if(ch=='-'){
			flag=1;
		}
		if(ch>='0'&&ch<='9'||ch>='A'&&ch<='F'||ch>='a'&&ch<='f'){		
			if(ch>='0'&&ch<='9'){
				res=res*16+ch-'0';
			}else if(ch>='A'&&ch<='F'){
				res=res*16+ch-'A'+10;
			}else if(ch>='a'&&ch<='f'){
				res=res*16+ch-'a'+10;
			}
			if(firstn&&flag){
				rf=-1;				
			}
			firstn=0;
		}
	}
	printf("%ld",res*rf);
	return 0;
}
