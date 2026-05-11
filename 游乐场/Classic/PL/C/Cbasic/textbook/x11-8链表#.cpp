struct ListNode *readlist(){
	int size=sizeof(struct ListNode);
	struct ListNode *p=NULL,*head=NULL,*tail=NULL;
	int num;
	scanf("%d",&num);
	while(num!=-1){
		p=(struct ListNode*)malloc(size);
		p->data=num;
		p->next=NULL;
		if(head==NULL){
			head=p;
		}else{
			tail->next=p;
		}
		tail=p;
		scanf("%d",&num);
	}
	return head;
}
struct ListNode *deletem( struct ListNode *L, int m ){
	struct ListNode *p=L,*p1=NULL,*p2=NULL;
	while(p!=NULL&&p->data==m){
		p1=p->next;
		free(p);
		p=p1;
	}
	
	if(p!=NULL){
		p1=p;
		p2=p1->next;
		while(p2!=NULL){
			if(p2->data==m){
				p1->next=p2->next;	
				free(p2);
			}else{
				p1=p2;
			}	
			p2=p1->next;
		}
	}
	return p;
}
