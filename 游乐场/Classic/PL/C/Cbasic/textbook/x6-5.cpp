int prime( int p ){
	int flag=1;
	if(p==1){
		flag=0;
	}else{
		for(int i=2;i<=sqrt(p);i++){
			if(p%i==0){
				flag=0;
				break;
			}
		}
	}
	return flag;
}
void Goldbach( int n ){
	for(int i=2;i<=n;i++){
		int pf=prime(i),qf=prime(n-i);
		if(pf&&qf){
			printf("%d=%d+%d",n,i,n-i);
			break;
		}
	}
}
