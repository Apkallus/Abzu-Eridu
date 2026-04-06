void delchar( char *str, char c ){
	int si=0;
	for(si=0;str[si]!='\0';si++){
	}
	
	for(int i=1;i<=si;i++){
		for(int k=0;k<=si-i;k++){
			if(str[k]==c){
				char temp=str[k];
				str[k]=str[k+1];
				str[k+1]=temp;
			}
		}
	}
}
