int f( int n ){
	int res;
	if(n==0){
		res=0;
	}else if(n==1){
		res=1;
	}else{
		res=f(n-2)+f(n-1);
	}
	return res;
}
