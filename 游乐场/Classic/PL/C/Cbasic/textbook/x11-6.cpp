char *search( char *s, char *t ){
	int i,k;
	char *p=NULL;
	for(i=0;s[i]!='\0';i++){
		int flag=1;
		if(s[i]==t[0]){
			for(k=0;t[k]!='\0';k++){				
				if(t[k]!=s[i+k]){
					flag=0;
					break;
				}
			}
			if(flag){
				p=s+i;
				break;
			}	
		}	
	}
	return p;
}
