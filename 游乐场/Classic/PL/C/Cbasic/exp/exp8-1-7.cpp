void ArrayShift( int a[], int n, int m ){
	m=m%n;
	int b[MAXN];
	for(int i=0;i<=n-1;i++){
		if(i+m<=n-1){
			b[i+m]=a[i];
		}else{
			b[i+m-(n-1)-1]=a[i];
		}
	}
	for(int i=0;i<=n-1;i++){
		a[i]=b[i];
	}
}
