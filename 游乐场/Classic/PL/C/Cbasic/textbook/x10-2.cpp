double fact( int n ){
	if(n==0||n==1){
		return 1;
	}else{
		return n*fact(n-1);
	}
}
double factsum( int n ){
	int sum=0;
	for(int i=1;i<=n;i++){
		sum=sum+fact(i);
	}
	return sum;
}
