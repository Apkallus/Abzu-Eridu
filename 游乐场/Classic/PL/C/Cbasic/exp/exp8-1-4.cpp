void sort( int a[], int n ){
	for(int i=1;i<=n-1;i++){
		for(int k=0;k<=n-1-i;k++){
			if(a[k]>a[k+1]){
				int temp=a[k];
				a[k]=a[k+1];
				a[k+1]=temp;
			}
		}
	}
}
