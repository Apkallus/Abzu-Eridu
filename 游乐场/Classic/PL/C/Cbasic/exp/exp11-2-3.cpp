struct ListNode *createlist(){
	struct ListNode t,*p,*head=NULL;
	scanf("%d",&t.data);
	while(t.data!=-1){
		t.next=NULL;
		p=(struct ListNode*)malloc(sizeof(struct ListNode));
		*p=t;
		if(head==NULL){
			head=p;
		}else{
			p->next=head;
			head=p;
		}
		scanf("%d",&t.data);
	}
	return head;
}
