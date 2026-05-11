double fact( int n ){
	double res;
	if(n==0||n==1){
		res=1;
	}else{
		res=n*fact(n-1);
	}
	return res;
}
double factsum( int n ){
	double sum=0;
	for(int i=1;i<=n;i++){
		sum+=fact(i);
	}
	return sum;
}
