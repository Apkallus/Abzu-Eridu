double fn( double x, int n ){
	double res;
	if(n==1){
		res=x;
	}else{
		int flag;
		if(n%2==0){
			flag=-1;
		}else{
			flag=1;
		}
		double num=1;
		int i;
		for(i=1;i<=n;i++){
			num=num*x;
		}
		res=flag*num+fn(x,n-1);

	}
	return res;
}
