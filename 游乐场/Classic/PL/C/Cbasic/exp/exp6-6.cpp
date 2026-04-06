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
void Goldbach( int n ){
	for(int i=2;i<n;i++){	
		if(prime(i)&&prime(n-i)){
			printf("%d=%d+%d",n,i,n-i);
			break;
		}
	}
}
