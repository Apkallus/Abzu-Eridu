int IsSquare( int n ){
	int res=0;
	double sq=sqrt(n);
	long int sqi=(int)sq;
	if(sq-sqi==0){
		res=1;
	}
	return res;
}
