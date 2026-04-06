double funcos( double e, double x ){
	double flag=1,item=1,fenzi=1,fenmu=1,nfenmu=0,sum=0;
	do{
		item=fenzi/fenmu;
		sum=sum+flag*item;
		printf("fenzi=%lf%,fenmu=%lf\n",fenzi,fenmu);
		fenzi=fenzi*x*x;
		fenmu=fenmu*(nfenmu+1)*(nfenmu+2);
		nfenmu=nfenmu+2;
		flag=-flag;
		
	}while(item>=e);
	return sum;
}



