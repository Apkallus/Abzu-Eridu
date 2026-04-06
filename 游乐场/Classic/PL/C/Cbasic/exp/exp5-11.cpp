int gcd( int x, int y ){
	int res;
	for(int i=x;i>0;i--){
		if(x%i==0&&y%i==0){
			res=i;
			break;
		}
	}
	return res;
}
