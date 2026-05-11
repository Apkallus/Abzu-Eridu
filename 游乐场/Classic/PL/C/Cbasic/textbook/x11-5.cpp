char *match( char *s, char ch1, char ch2 ){
	int ich1=-1,ich2=-1,i;
	for(i=0;s[i]!='\0';i++){
		if(ich1==-1&&s[i]==ch1){
			ich1=i;
		}
		if(ich2==-1&&s[i]==ch2){
			ich2=i;
		}
	}
	char *p=s+i;
	if(ich1>-1){
		if(ich2==-1){
			for(int i=ich1;s[i]!='\0';i++){
				putchar(s[i]);
			}
		}else{
			for(int i=ich1;i<=ich2;i++){
				putchar(s[i]);
			}
		}				
		p=s+ich1;
	}
	putchar('\n');
	return p;
}
