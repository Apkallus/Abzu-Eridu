struct complex multiply(struct complex x, struct complex y){
	struct complex res;
	res.real=x.real*y.real-x.imag*y.imag;
	res.imag=x.real*y.imag+y.real*x.imag;
	return res; 
}
