double funcos( double e, double x ){
	double item,sum=0,fenmu=1;
	int flag=1,count=0;
	do{
		item=flag*pow(x,count)/fenmu;
		sum=sum+item;
		count=count+2;
		flag=-flag;
		fenmu=fenmu*(count-1)*count;
	}while(fabs(item)>=e);
	return sum;
}
