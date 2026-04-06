int search( int n ){
	int count=0;
	for(int i=sqrt(101)+1;i<=sqrt(n);i++){
		int res=i*i,a[3];
		for(int k=0;k<=3-1;k++){
			a[k]=res%10;
			res/=10;
		}
		int flag=0;
		for(int j=0;j<=3-1-1;j++){
			for(int g=j+1;g<=3-1;g++){
				if(a[j]==a[g]){
					count++;
					flag=1;
					break;
				}
			}
			if(flag){
				break;
			}
		}
	}
	return count;
}
