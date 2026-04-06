void delchar( char *str, char c ){
	for(int i=0;str[i]!='\0';i++){
		if(c==str[i]){
			int k;
			for(k=i+1;str[k]!='\0';k++){
				str[k-1]=str[k];
			}
			str[k-1]='\0';
			i--;
		}
	}
}
