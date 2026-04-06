double P( int n, double x ){
	double res;
	if(n==0){
		res=1;
	}else if(n==1){
		res=x;
	}else{
		res=((2*n-1)*P(n-1,x)-(n-1)*P(n-2,x))/n;
	}
	return res;
}
