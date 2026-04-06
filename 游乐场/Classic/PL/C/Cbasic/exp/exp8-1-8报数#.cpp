void CountOff( int n, int m, int out[] ){
	for(int i=0;i<=n-1;i++){
		out[i]=0;
	}
	int start=0,outn,count=0;
	outn=m%(n-count);
		if(outn==0){
			outn=(n-count);
		}
		
	while(count<n){
			
		int i;
		for(i=start;i<=n-1;i++){
			if(out[i]==0){
				outn--;
			}
//			if(outn==1){
			if(outn==0){
				count++;
				out[i]=count;
				start=i;
				
				if(count!=n){
					outn=m%(n-count);//%0±¨´í 
					if(outn==0){
						outn=(n-count);
					}					
				}
				break;
			}
		}	
		if(i>n-1){
			start=0;
		}	
		
	}
		
}
