int Ack( int m, int n ){
	long int res;
	if(m==0){
		res=n+1;
	}else if(n==0&&m>0){
		res=Ack(m-1,1);
	}else{
		res=Ack(m-1,Ack(m,n-1));
	}
	return res;
}
