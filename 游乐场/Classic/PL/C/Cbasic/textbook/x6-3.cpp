int factorsum( int number ){
	int sum=0;
	for(int i=1;i<=number-1;i++){
		if(number%i==0){
			sum=sum+i;
		}
	}
	return sum;
}
void PrintPN( int m, int n ){
	int flag=0;
	for(int i=m;i<=n;i++){
		if(i==factorsum(i)){
			printf("%d",i);
			flag=1;
			for(int j=1;j<=i-1;j++){
				if(j==1){
					printf(" = %d",j);
				}else if(i%j==0){
					printf(" + %d",j);
				}
			}
			putchar('\n');
			
		}
	}
	if(!flag){
		printf("No perfect number");
	}
}
