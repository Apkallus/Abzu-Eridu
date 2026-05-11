int narcissistic( int number ){
	int n=0,tn,tn2;
	tn=tn2=number;
	do{
		tn=tn/10;
		n++;
	}while(tn!=0);
	
	int sum=0;
	do{
		sum=sum+pow(tn2%10,n);
		tn2=tn2/10;
	}while(tn2!=0);
	
	int flag=0;
	if(sum==number){
		flag=1;
	}
	return flag;
}
void PrintN( int m, int n ){
	int i;
	for(i=m+1;i<=n-1;i++){
		if(narcissistic(i)){
			printf("%d\n",i);
		}
	}
}
