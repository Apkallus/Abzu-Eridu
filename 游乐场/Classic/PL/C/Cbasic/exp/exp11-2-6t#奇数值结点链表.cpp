struct ListNode *readlist(){
	struct ListNode *p,temp,*head=NULL,*tail=NULL;
	scanf("%d",&temp.data);
	while(temp.data!=-1){
		temp.next=NULL;
		p=(struct ListNode*)malloc(sizeof(struct ListNode));
		*p=temp;
		if(head==NULL){
			head=p;
		}else{
			tail->next=p;
		}
		tail=p;
		scanf("%d",&temp.data);
	}
	return head;
}
struct ListNode *getodd( struct ListNode **L ){
	struct ListNode *po1,*po2,*jhead,*jtail;
	po2=*L;	
	jhead=jtail=NULL;

	while(po2!=NULL){
		if((*L)->data%2==1){
			*L=po2->next;
			if(jhead==NULL){
				jhead=po2;
			}else{
				jtail->next=po2;
			}
			jtail=po2;
			jtail->next=NULL;
			po2=*L;			
		}else{
			if(po2->data%2==1){
				po1->next=po2->next;
				
				if(jhead==NULL){
					jhead=po2;
				}else{
					jtail->next=po2;
				}
				jtail=po2;
				jtail->next=NULL;				
			}else{
				po1=po2;		
			}
			po2=po1->next;
		}			
	} 

	return jhead;
}
