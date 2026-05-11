char *getmonth( int n ){
	char *p=NULL,*a[12]={"January","February","March","April","May","June","July","August","September","October","November","December"};

	if(n>=1&&n<=12){
		p=a[n-1];
	}
	return p;
}
