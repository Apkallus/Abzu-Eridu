#include<stdio.h>
#include<math.h>
#include<string.h>
struct ti{
	int hh;
	int mm;
	int ss;
};
int main(void){

	
	struct ti time;
	scanf("%d:%d:%d",&time.hh,&time.mm,&time.ss);	
		
	int n;
	scanf("%d",&n);
	if(time.ss+n>=60){
		time.mm++;
	}
	time.ss=(time.ss+n)%60;
	if(time.mm>=60){
		time.hh++;
		time.mm%=60;
	}
	if(time.hh>=24){
		time.hh%=24;
	}
	printf("%02d:%02d:%02d",time.hh,time.mm,time.ss);	
	return 0;
}
