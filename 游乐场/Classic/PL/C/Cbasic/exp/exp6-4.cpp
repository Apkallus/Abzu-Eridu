int factorsum( int number ){
	int sum=0;
	for(int i=1;i<=number/2;i++){
		if(number%i==0){
			sum+=i;
		}
	}
	return sum;
}
void PrintPN( int m, int n ){
	int flag=0;
	for(int i=m;i<=n;i++){
		if(i==factorsum(i)){
			printf("%d = ",i);
			flag=1;
			for(int k=1;k<=i/2;k++){
				if(i%k==0){
					if(k==1){
						printf("%d",k);
					}else{
						printf(" + %d",k);
					}
					
				}
			}
			putchar('\n');
		}
	}
	if(flag==0){
		printf("No perfect number");
	}
}
