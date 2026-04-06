void CountOff( int n, int m, int out[] ){
	
	for(int i=0;i<=n-1;i++){
		out[i]=0;
	}
	
	int countout=0,lastindex=0;
	while(countout!=n){
		int countm=0,enter1=0;
		while(countm!=m){			
			int i;
			if(enter1==0){
				i=lastindex;
				enter1=1;
			}else{
				i=0;
			}
			for(;i<=n-1;i++){
				if(out[i]==0){
					countm++;
					if(countm==m){	
						countout++;
						out[i]=countout;
						lastindex=i;			
						break;			
					}
				}
			}
		}
	}
}
