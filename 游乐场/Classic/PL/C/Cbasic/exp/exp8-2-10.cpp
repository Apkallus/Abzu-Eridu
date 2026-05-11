#include<stdio.h>
#include<math.h>
#include<string.h>
void pnumber(void){
	char ch;
	int num,res=0;
	for(int i=0;i<=8-1;i++){
		ch=getchar();
		num=ch-'0';
		res=res*2+num;
	}
	printf("%d",res);
}
int main(void){
	
	for(int i=1;i<=4;i++){
		pnumber();
		if(i<4){
			putchar('.');
		}
	}
	
	
	return 0;
}
