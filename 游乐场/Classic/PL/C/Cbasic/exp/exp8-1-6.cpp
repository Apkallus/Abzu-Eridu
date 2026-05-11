void f( char *p ){
	int count=0;
	while(p[count]!='\0'){
		count++;
	}
	count--;
	for(int i=0;i<count;i++,count--){
		int temp=p[i];
		p[i]=p[count];
		p[count]=temp;
	}
}
