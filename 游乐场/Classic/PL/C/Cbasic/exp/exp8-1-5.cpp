int search( int list[], int n, int x ){
	int flag=-1;
	for(int i=0;i<=n-1;i++){
		if(list[i]==x){
			flag=i;
			break;
		}
	}
	return flag;
}
