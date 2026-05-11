void ArrayShift( int a[], int n, int m ){
	m=m%n;
	for(int k=1;k<=m;k++){
		int temp=a[n-1];
		for(int i=n-1;i>=1;i--){
			a[i]=a[i-1];
		}
		a[0]=temp;
	}
}
