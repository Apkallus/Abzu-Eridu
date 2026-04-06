int getindex( char *s ){
	char *a[7]={"Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"};
	int res=-1;
	for(int i=0;i<=7-1;i++){
		if(strcmp(s,a[i])==0){
			res=i;
			break;
		}
	}
	return res;
}
