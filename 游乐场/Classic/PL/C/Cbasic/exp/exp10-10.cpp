void printdigits( int n ){
	char ch; 
	if(n/10!=0){
		printdigits(n/10);		
	}
	
	ch=n%10+'0';
	printf("%c\n",ch);
}

