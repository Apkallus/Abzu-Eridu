struct ListNode *reverse( struct ListNode *head ){
	struct ListNode *p,*p1,*p2,*nhead=NULL,*bp=NULL;
	
	p=head;
	while(p!=NULL){
		head=head->next;
		if(bp==NULL){
			p->next=NULL;
		}else{
			p->next=bp;
		}
		bp=p;
		p=head;
	}
	return bp;
}
