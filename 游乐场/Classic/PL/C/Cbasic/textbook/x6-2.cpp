int fn( int a, int n ){
	int res=0;
	for(int i=1;i<=n;i++){
		res=res*10+a;
	}
	return res;
}
/*
int SumA( int a, int n ){
	int sum=0;
	for(int i=1;i<=n;i++){
		sum=sum+fn(a,i);
	}
	return sum;
}
*/
int SumA( int a, int n ){
	int sum=0,item=0;
	for(int i=1;i<=n;i++){
		item=item*10+a;
		sum=sum+item;
	}
	return sum;
}
