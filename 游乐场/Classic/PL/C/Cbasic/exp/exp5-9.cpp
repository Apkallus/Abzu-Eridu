int narcissistic( int number ){
	int sum=0,res=0,num=number,count=0,item;
	while(num!=0){
		num=num/10;
		count++;
	}	
	num=number;
	while(num!=0){
		item=num%10;
		int itemres=1;
		for(int i=1;i<=count;i++){
			itemres=itemres*item;
		}
		sum+=itemres;
		num=num/10;
	}
	if(sum==number){
		res=1;
	}
	return res;
}
void PrintN( int m, int n ){
	for(int i=m+1;i<=n-1;i++){
		if(narcissistic(i)){
			printf("%d\n",i);
		}
	}
}
