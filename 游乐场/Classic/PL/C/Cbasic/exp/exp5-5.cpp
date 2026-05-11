int prime( int p ){
	int res=1;
	if(p>1){
		for(int i=2;i<=sqrt(p);i++){
			if(p%i==0){
				res=0;
				break;
			}
		}
	}else{
		res=0;
	}
	return res;
}
int PrimeSum( int m, int n ){
	int sum=0;
	for(int i=m;i<=n;i++){
		if(prime(i)){
			sum+=i;
		}
	}
	return sum;
}
