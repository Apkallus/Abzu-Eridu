int reverse( int number ){
	int res=0;
	do{
		res=res*10+number%10;
		number=number/10;
	}while(number!=0);
	return res;
}
