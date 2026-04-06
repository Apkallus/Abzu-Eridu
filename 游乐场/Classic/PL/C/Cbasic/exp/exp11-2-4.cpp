struct ListNode *createlist(){
	struct ListNode t,*p,*head=NULL,*tail=NULL;
	scanf("%d",&t.data);
	while(t.data!=-1){
		t.next=NULL;
		p=(struct ListNode*)malloc(sizeof(struct ListNode));
		*p=t;
		if(head==NULL){
			head=p;
		}else{
			tail->next=p;
		}
		tail=p;
		scanf("%d",&t.data);
	}
	return head;
}
struct ListNode *deleteeven( struct ListNode *head ){
	struct ListNode *p1,*p2;
	while(head!=NULL&&head->data%2==0){
		p2=head;
		head=head->next;
		free(p2);
	}
	if(head!=NULL){
		p1=head;
		p2=p1->next;
		while(p2!=NULL){
			if(p2->data%2==0){
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
