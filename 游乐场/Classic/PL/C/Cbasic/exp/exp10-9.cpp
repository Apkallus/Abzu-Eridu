void dectobin( int n ){
	if(n/2!=0){
		dectobin(n/2);		
	}
	
	if(n%2==0){
		putchar('0');
	}else{
		putchar('1');
	}
}
