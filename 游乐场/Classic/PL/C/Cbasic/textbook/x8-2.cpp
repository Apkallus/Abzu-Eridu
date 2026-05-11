int search( int list[], int n, int x ){
	int i,res=-1;
	for(i=0;i<=n-1;i++){
		if(list[i]==x){
			res=i;
			break;
		}
	}
	return res;
}
