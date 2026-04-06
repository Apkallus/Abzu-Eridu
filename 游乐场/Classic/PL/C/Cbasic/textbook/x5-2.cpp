int even( int n ){
	int res;
	if(n%2==0){
		res=1;
	}else{
		res=0;
	}
	return res;
}

int OddSum( int List[], int N ){
	int i,sum=0;
	for(i=0;i<=N-1;i++){
		if(even(List[i])==0){
			sum=sum+List[i];
		}
	}
	return sum;
}









