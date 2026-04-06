char *search( char *s, char *t ){
	char *p=NULL;
	for(int i=0;s[i]!='\0';i++){
		if(s[i]==t[0]){
			int k;
			for(k=0;t[k]!='\0';k++){
				if(s[i+k]!=t[k]){
					break;
				}
			}
			if(t[k]=='\0'){
				p=s+i;
				break;
			}
		}
	}
	return p;
}
