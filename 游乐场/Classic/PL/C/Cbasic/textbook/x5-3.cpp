double dist( double x1, double y1, double x2, double y2 ){
	double res,a,b;
	a=fabs(x1-x2);
	b=fabs(y1-y2);
	
	res=sqrt(a*a+b*b);
	return res;
}
