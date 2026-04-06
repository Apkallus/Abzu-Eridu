#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct node{
	char code[8];
	struct node *next;
};
int main(void){
	struct node *head,*tail,*p;
	int i,n,count;
	char str[8];
	int size=sizeof(struct node);
	head=NULL;
	gets(str);
	while(strcmp(str,"#")!=0){
		p=(struct node*)malloc(size);
		strcpy(p->code,str);
		p->next=NULL;
//		head=p->next;
		if(head==NULL){
			head=p;
		}else{
			tail->next=p;
		}
//		head=p;	
		tail=p;	
		gets(str);
	}
	count=0;
//	for(p=head;p->next!=NULL;p=p->next){
	for(p=head;p!=NULL;p=p->next){
		if(p->code[1]=='0'&&p->code[2]=='2'){
			count++;
		}
	}
	printf("%d\n",count);
	return 0;
}
