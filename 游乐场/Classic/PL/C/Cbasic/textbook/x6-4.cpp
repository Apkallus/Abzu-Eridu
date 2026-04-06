int fib( int n ){
	int n1,n2,n3;
	n1=n2=1;
	n3=0;
	if(n<3){
		n3=1;
	}else{
		for(int i=3;i<=n;i++){
			n3=n1+n2;
			n1=n2;
			n2=n3;
		}
	}
	
	return n3;
}
void PrintFN( int m, int n ){
	int res,count=0;
	for(int j=1;(res=fib(j))<=n;j++){
		if(res>=m){
			if(count==0){
				printf("%d",res);
				count=1;
			}else{
				printf(" %d",res);
			}
		}
	}
	
	if(count==0){
		printf("No Fibonacci number");
	}
}






