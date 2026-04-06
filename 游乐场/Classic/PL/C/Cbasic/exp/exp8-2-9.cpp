void f( long int x, char *p ){
	int count=0,flag=0;
	if(x<0){
		x=-x;
		p[0]='-';
		count++;
		flag=1;
	}
	do{
		int num=x%16;
		if(num<10){
			p[count]=num+'0';
		}else{
			p[count]=num-10+'A';
		}
		x/=16;
		count++;
	}while(x!=0);
	p[count]='\0';
	for(int s=flag,e=count-1;s<e;s++,e--){
		char t=p[s];
		p[s]=p[e];
		p[e]=t;
	}
}
