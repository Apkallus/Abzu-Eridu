struct ListNode {
    char code[8];
    struct ListNode *next;
};
int countcs( struct ListNode *head ){
	struct ListNode *p=head;
	int count=0;
	while(p!=NULL){
		if(p->code[1]=='0'&&p->code[2]=='2'){
			count++;
		}
		p=p->next;
	}
	return count;
}
