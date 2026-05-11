void strmcpy( char *t, int m, char *s ){
	int counti=0;
	while(t[counti]!='\0'){
		counti++;
	}
	if(m-1<=counti){
		int i,si;
		for(i=m-1,si=0;i<=counti;i++,si++){
			s[si]=t[i];
		}	
	}
}
