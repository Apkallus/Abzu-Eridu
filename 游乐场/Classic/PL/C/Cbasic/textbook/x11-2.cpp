int getindex( char *s ){
	char *a[7]={"Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"};
	int i,res=-1;
	for(i=0;i<=7-1;i++){
		if(strcmp(s,a[i])==0){
			res=i;
			break;
		}
	}
	return res;
}
