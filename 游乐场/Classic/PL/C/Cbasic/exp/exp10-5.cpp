double fn( double x, int n ){
	double res,flag;
	if(n%2==1){
		flag=1;
	}else{
		flag=-1;
	}
	if(n==1){
		res=x*flag;
	}else{
		double s=1;
		for(int i=1;i<=n;i++){
			s=s*x;
		}
		res=s*flag+fn(x,n-1);
	}
	return res;
}
