int fib( int n ){
	int n1=1,n2=1,num;
	if(n>=3){
		for(int i=3;i<=n;i++){
			num=n1+n2;
			n1=n2;
			n2=num;
		}
	}else{
		num=1;
	}
	return num;
}
void PrintFN( int m, int n ){
	int item,count=0;
	for(int i=1;(item=fib(i))<=n;i++){
		if(item>=m){
			if(count==0){
				printf("%d",item);
			}else{
				printf(" %d",item);
			}
			count=1;
		}
	}
	if(count==0){
		printf("No Fibonacci number");
	}
}
