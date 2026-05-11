bool palindrome( char *s ){
	int p,q,i,res=1;
	for(i=0;s[i]!='\0';i++){
	}
	q=i-1;
	for(p=0;p<=q;p++,q--){
		if(s[p]!=s[q]){
			res=0;
			break;
		}
	}
	return res;
}
