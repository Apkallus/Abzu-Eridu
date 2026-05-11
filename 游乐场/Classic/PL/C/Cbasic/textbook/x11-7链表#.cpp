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
struct ListNode *getodd( struct ListNode **L ){
	struct ListNode *p=*L,*oldhead1=*L,*oldhead2=NULL,*newhead=NULL,*newtail=NULL;
	while(p!=NULL&&p->data%2!=0){

		if(newhead==NULL){
			newhead=p;
		}else{
			newtail->next=p;
		}
		newtail=p;
		
		oldhead1=p->next;
		p->next=NULL;
		*L=p=oldhead1;
	}
	
	
	if(p!=NULL){
		oldhead1=p;
		oldhead2=oldhead1->next;
		while(oldhead2!=NULL){
	
			if(oldhead2->data%2!=0){			
				if(newhead==NULL){
					newhead=oldhead2;
				}else{
					newtail->next=oldhead2;
				}	
				newtail=oldhead2;
				
				oldhead1->next=oldhead2->next;
				oldhead2->next=NULL;		
			}else{
				oldhead1=oldhead2;
			}
			oldhead2=oldhead1->next;
		}
	}
	return newhead;
}
