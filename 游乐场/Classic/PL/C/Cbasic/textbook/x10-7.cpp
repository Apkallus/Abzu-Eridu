void dectobin( int n ){
	int res;
	if(n%2==0){
		res=0;
	}else{
		res=1;
	}
	
	if(n/2!=0){
		dectobin(n/2);
	}
	printf("%d",res);
}
