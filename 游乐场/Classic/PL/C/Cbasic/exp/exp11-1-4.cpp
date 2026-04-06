int max_len( char *s[], int n ){
	int maxn=0;
	for(int i=0;i<=n-1;i++){
		if(i==0){
			maxn=strlen(s[i]);
		}else{
			if(maxn<strlen(s[i])){
				maxn=strlen(s[i]);
			}
		}
	}
	return maxn;
}
