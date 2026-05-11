int Ack( int m, int n ){
	int res;
	if(m==0){
		res=n+1;
	}else if(n==0&&m>0){
		res=Ack(m-1,1);
	}else if(m>0&&n>0){
		res=Ack(m-1,Ack(m,n-1));
	}
	return res;
}
