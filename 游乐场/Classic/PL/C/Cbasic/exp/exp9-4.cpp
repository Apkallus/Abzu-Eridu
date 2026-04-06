struct complex multiply(struct complex x, struct complex y){
	struct complex res;
	res.real=x.real*y.real-x.imag*y.imag;
	res.imag=x.imag*y.real+x.real*y.imag;
	return res;
}
