#include<stdio.h>
struct time {
	int hh,mm,ss;
};

int main(void){
	
	struct time t;
	scanf("%d:%d:%d",&t.hh,&t.mm,&t.ss);
	int s;
	scanf("%d",&s);
	
	if(t.ss+s<60){
		t.ss=t.ss+s;
	}else{
		t.ss=t.ss+s-60;
		t.mm++;
		if(t.mm==60){
			t.mm=0;
			t.hh++;
		}if(t.hh==24){
			t.hh=0;
		}
	}
	printf("%02d:%02d:%02d",t.hh,t.mm,t.ss);
		
	 return 0;
}
