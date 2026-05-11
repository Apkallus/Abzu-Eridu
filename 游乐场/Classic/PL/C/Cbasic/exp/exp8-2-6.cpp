void StringCount( char *s ){
	int upletter=0,lowletter=0,blank=0,digit=0,other=0;
	for(int i=0;s[i]!='\0';i++){
		if(s[i]>='A'&&s[i]<='Z'){
			upletter++;
		}else if(s[i]>='a'&&s[i]<='z'){
			lowletter++;
		}else if(s[i]>='0'&&s[i]<='9'){
			digit++;
		}else if(s[i]==' '){
			blank++;
		}else{
			other++;
		}
	}
	printf("%d %d %d %d %d",upletter,lowletter,blank,digit,other);
}
