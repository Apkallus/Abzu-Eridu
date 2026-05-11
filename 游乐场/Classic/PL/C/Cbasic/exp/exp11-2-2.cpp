struct stud_node {
    int              num;      /*??*/
    char             name[20]; /*??*/
    int              score;    /*??*/
    struct stud_node *next;    /*?????????*/
};
struct stud_node *createlist(){
	struct stud_node t,*p,*head=NULL,*tail=NULL;
	scanf("%d",&t.num);
	while(t.num!=0){
		scanf("%s%d",t.name,&t.score);
		t.next=NULL;
		p=(struct stud_node*)malloc(sizeof(struct stud_node));
		*p=t;
		if(head==NULL){
			head=p;
		}else{
			tail->next=p;
		}
		tail=p;
		scanf("%d",&t.num);
	}
	return head;
}
struct stud_node *deletelist( struct stud_node *head, int min_score ){
	struct stud_node *p1,*p2;
	while(head!=NULL&&head->score<min_score){
		p2=head;
		head=head->next;
		free(p2);
	}
	if(head!=NULL){
		p1=head;
		p2=p1->next;
		while(p2!=NULL){
			if(p2->score<min_score){
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
