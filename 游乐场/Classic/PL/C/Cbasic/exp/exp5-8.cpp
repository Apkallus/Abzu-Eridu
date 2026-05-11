int CountDigit( int number, int digit ){
	int count=0;
	if(number<0){
		number=-number;
	}
	do{
		if(number%10==digit){
			count++;
		}
		number/=10;
	}while(number!=0);
	return count;
}
