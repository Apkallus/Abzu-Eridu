void strmcpy( char *t, int m, char *s ){
	
	int k;
	for(k=0;t[k]!='\0';k++){	
	}
	if(m-1<=k){
		int si=0;
		for(int i=m-1;t[i]!='\0';i++){
			s[si]=t[i];
			si++;
		}
		s[si]='\0';
	}

}
