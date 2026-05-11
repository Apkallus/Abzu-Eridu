void input(){
	struct stud_node t,*p;
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
}
