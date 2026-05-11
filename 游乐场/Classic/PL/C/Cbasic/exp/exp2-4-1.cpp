int is( int number ){
	int res=0,sum=0;
	while(number!=0){
		sum+=number%10;
		number/=10;
	}
	if(sum==5){
		res=1;
	}
	return res;
}
void count_sum( int a, int b ){
	int count=0,sum=0;
	for(int i=a;i<=b;i++){
		if(is(i)){
			sum+=i;
			count++;
		}
	}
	printf("count = %d, sum = %d",count,sum);
}
