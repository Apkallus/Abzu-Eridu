struct ListNode *mergelists(struct ListNode *list1, struct ListNode *list2){
	struct ListNode *pa,*pb,*p1,*p2;
	
	pa=list1;
	p1=list2;
	if(pa!=NULL){
		pb=pa->next;	
	}
	if(p1!=NULL){	
		p2=p1->next;
	}
	while(pa!=NULL&&p1!=NULL){
		if(pa->data<=p1->data){
			pa->next=p1;
			list2=pa;
			list1=pb;
			
			pa=pb;
			if(pa!=NULL){
				pb=pa->next;	
			}
		}else if(p2!=NULL&&pa->data>p1->data&&pa->data<=p2->data){
			p1->next=pa;
			pa->next=p2;
			list1=pb;
			
			p1=pa;
			pa=pb;
			if(pa!=NULL){
				pb=pa->next;	
			}			
		}else if(p2!=NULL&&pa->data>p1->data&&pa->data>p2->data){
			p1=p2;
			if(p1!=NULL){	
				p2=p1->next;
			}
		}else if(p2==NULL&&pa->data>p1->data){
			p1->next=pa;
			list1=NULL;
			break;
		}
	}
	return list2 ;
}
