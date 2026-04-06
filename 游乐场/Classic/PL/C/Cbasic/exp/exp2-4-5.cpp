double mypow( double x, int n ){
	double res;
	if(x!=0){
		res=1;
		for(int i=1;i<=n;i++){
			res=res*x;
		}
	}else{
		res=0;
	}

	return res;
}
