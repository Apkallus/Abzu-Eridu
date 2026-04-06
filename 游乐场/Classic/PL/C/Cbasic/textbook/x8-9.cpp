void StringCount( char *s ){
	int caplt,lowlt,blank,digt,other;
	caplt=lowlt=blank=digt=other=0;
	for(int i=0;s[i]!='\0';i++){
		if(s[i]>='A'&&s[i]<='Z'){
			caplt++;
		}else if(s[i]>='a'&&s[i]<='z'){
			lowlt++;
		}else if(s[i]==' '){
			blank++;
		}else if(s[i]>='0'&&s[i]<='9'){
			digt++;
		}else{
			other++;
		}
	}	
	printf("%d %d %d %d %d",caplt,lowlt,blank,digt,other);
}

