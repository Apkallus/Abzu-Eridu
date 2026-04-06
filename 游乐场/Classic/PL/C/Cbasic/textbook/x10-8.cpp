void printdigits( int n ){
	
	if(n/10!=0){
		printdigits(n/10);
	}
	printf("%d",n%10);
}
