struct ListNode *readlist(){
	int num,size=sizeof(struct ListNode);
	struct ListNode *p=NULL,*head=NULL,*tail=NULL;
	
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
	struct ListNode *p=L,*p1,*p2;
	while(p!=NULL&&p->data==m){
		L=p->next;
		free(p);
		p=L;
	}
	if(L!=NULL){
		p1=L;
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
	return L;
}
