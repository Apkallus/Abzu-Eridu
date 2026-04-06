int prime( int p ){
	int flag=1,i;
	for(i=2;i<=sqrt(p);i++){
		if(p%i==0){
			flag=0;
			break;
		}
	}
	if(p<=1){
		flag=0;
	}
	return flag;
}
int PrimeSum( int m, int n ){
	int i,sum=0;
	for(i=m;i<=n;i++){
		if(prime(i)){
			sum=sum+i;
		}
	}
	return sum;
}
