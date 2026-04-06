double calc_pow( double x, int n ){
	double res;
	if(n==0){
		res=1;
	}else if(n==1){
		res=x;
	}else{
		res=x*calc_pow(x,n-1);
	}
	return res;
}

