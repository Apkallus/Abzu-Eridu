#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct info{
	char state;
	int num;
	int time;
};
void set0(struct info *p,int n){
	for(int i=0;i<=n-1;i++,p++){
		p->state=NULL;
		p->num=0;
		p->time=0;
	} 
}
void parkin(struct info *p,int n,struct info *t){
	for(int i=0;i<=n-1;i++,p++){
		if(p->state==NULL){
			p->state='A';
			p->num=t->num;
			p->time=t->time;
		}
	}
}
int main(void){
	
	int n,count=0;
	scanf("%d",&n);
	
	struct info car[30],t,wait[10];
	set0(car,n);
	set0(wait,10);
	
	scanf("%c",&t.state);
	while(t.state!='E'){
		scanf("%d%d",&t.num,&t.time);
		if(t.state=='A'){
			parkin();
		}else if(t.state=='D'){
			parkout();
		}
		scanf("%c",&t.state);
	}
	
	return 0;
}
