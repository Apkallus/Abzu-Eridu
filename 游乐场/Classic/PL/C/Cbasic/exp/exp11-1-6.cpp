char *match( char *s, char ch1, char ch2 ){
	int ch1flag=0,ch2flag=0,index=0;
	char *pch1;
	while(*s!='\0'){
		if(*s==ch1&&ch1flag==0){
			ch1flag=1;
			pch1=s;
		}
		if(ch1flag==1&&ch2flag==0){
			putchar(*s);
		}
		if(*s==ch2){
			ch2flag=1;
		}
		s++;
		index++;
	}
	putchar('\n');
	if(ch1flag==0){
		pch1=s;
	}
	return pch1;
}
