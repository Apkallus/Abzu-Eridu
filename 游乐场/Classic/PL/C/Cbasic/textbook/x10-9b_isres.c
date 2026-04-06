int isres(int item){
	int res=1,i;
	if(item==1){
		res=0;
	}else{
		for(i=2;i<=item/2;i++){
			if(item%i==0){
				res=0;
				break;
			}
		}		
	}
	return res;
}
