int max_len( char *s[], int n ){
	int max=0;
	for(int i=0;i<=n-1;i++){
		if(i==0){
			max=strlen(s[i]);
		}else{
			if(max<strlen(s[i])){
				max=strlen(s[i]);
			}
		}
	}
	return max;
}
