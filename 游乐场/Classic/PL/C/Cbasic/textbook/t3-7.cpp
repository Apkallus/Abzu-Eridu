#include<stdio.h>
int main(void)
{
	int sc,tr;
	scanf("%d",&sc);
	
	if(sc>=90){
		tr='A';
	}else if(sc<90&&sc>=80){
		tr='B';
	}else if(sc<80&&sc>=70){
		tr='C';
	}else if(sc<70&&sc>=60){
		tr='D';
	}else if(sc<60){
		tr='E';
	}else{
		tr='er';
	}
	
	printf("%c",tr);
	
	return 0;
}
