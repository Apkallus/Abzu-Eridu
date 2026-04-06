int search( int n ){
	int count=0;
	for(int i=(int)sqrt(101)+1;i<=(int)sqrt(n);i++){
		int pow2=i*i;
		int a=pow2%10,b=pow2/10%10,c=pow2/100%10;
		if(a==b||a==c||b==c){
			count++;
		}
	}	
	return count;
}
