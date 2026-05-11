#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct stud_node{
	int num;
	char name[20];
	int score;
	struct stud_node *next;
};
int size=sizeof(struct stud_node);
struct stud_node * Create_Stu_Doc();
struct stud_node *InsertDoc(struct stud_node * head,struct stud_node * stud);
struct stud_node * DeleteDoc(struct stud_node * head);
void Print_Stu_Doc(struct stud_node *head);
int main(void){
	struct stud_node *head=NULL,*p,t;
	int choice;
	
	
	do{
		printf("1.creat 2.insert 3.delete 4.print 0.exit \n");
		scanf("%d",&choice);
		switch(choice){
			case 1:
				head=Create_Stu_Doc();
				break;
			case 2:
				printf("Input num,name and score:\n");
				scanf("%d%s%d",&t.num,t.name,&t.score);
				p=(struct stud_node *)malloc(size);
				*p=t;
				head=InsertDoc(head,p);				
				break;
			case 3:
				head=DeleteDoc(head);
				break;
			case 4:
				Print_Stu_Doc(head);
				break;
			case 0:
				break;
		}
	}while(choice!=0);
}
struct stud_node *Create_Stu_Doc(){
	struct stud_node *head,*p,t;
	
	head=NULL;
	printf("Input num,name and score:\n");
	scanf("%d",&t.num);
	while(t.num!=0){
		scanf("%s%d",t.name,&t.score);
		p=(struct stud_node *)malloc(size);
		*p=t;
		head=InsertDoc(head,p);
		scanf("%d",&t.num);
	}
	return head;
}
struct stud_node *InsertDoc(struct stud_node * head,struct stud_node * stud){
	struct stud_node *p,*p1,*p2; 
	
	p2=head;
	p=stud;
	if(head==NULL){
		head=p;
		head->next=NULL;
	}else{
		while((p->num>p2->num)&&(p2->next!=NULL)){
			p1=p2;
			p2=p2->next;
		}
		if(p->num<=p2->num){
			if(p2==head){
				head=p;
			}else{
				p1->next=p;				
			}
			p->next=p2;
		}else{
			p2->next=p;
			p->next=NULL;
		}
	}
	return head;
}
struct stud_node *DeleteDoc(struct stud_node * head){
	struct stud_node *p1,*p2; 
	int num;
	printf("input num:\n");
	scanf("%d",&num);
	
	while(head!=NULL&&head->num==num){
		p2=head;
		head=head->next;
		free(p2);
	}
	if(head!=NULL){
		p1=head;
		p2=p1->next;
		while(p2!=NULL){
			if(p2->num==num){
				p1->next=p2->next;
				free(p2);
			}else{
				p1=p2;			
			}
			p2=p1->next;
		}
	}
	return head;
}
void Print_Stu_Doc(struct stud_node * head){
	struct stud_node *p;
	if(head==NULL){
		printf("\n no records \n");
	}else{
		printf("num\tname\tscore\t\n");
		for(p=head;p!=NULL;p=p->next){
			printf("%d\t%s\t%d\n",p->num,p->name,p->score);
		}
	}
}
