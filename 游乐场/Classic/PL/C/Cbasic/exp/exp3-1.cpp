#include<stdio.h>
#include<math.h>
int main(void){
	
	double a,b,c,d;
	scanf("%lf%lf%lf",&a,&b,&c);
	
	d=b*b-4*a*c;
	
	if(a==0){
		if(b==0){
			if(c!=0){
				printf("Not An Equation");
			}else{
				printf("Zero Equation");
			}	
		}else{
			double res=-c/b;
			if(res<0&&res>-0.005){
				res=0;
			}
			printf("%0.2lf",res);
		}
	}else{
		if(d>=0){
			double x1,x2,low,up;
			x1=(-b+sqrt(d))/(2*a);
			x2=(-b-sqrt(d))/(2*a);
			if(x1<0&&x1>-0.005){
				x1=0;
			}
			if(x2<0&&x2>-0.005){
				x2=0;
			}
			if(x1!=x2){
				printf("%0.2f\n",x1);
				printf("%0.2f\n",x2);				
			}else{
				printf("%0.2f\n",x1);
			}

		}else{
			double real=-b/(2*a);
			if(real<0&&real>-0.005){
				real=0;
			}
			printf("%0.2f+%0.2fi\n",real,sqrt(-d)/(2*a));
			printf("%0.2f-%0.2fi\n",real,sqrt(-d)/(2*a));
		}
	}

	
	return 0;
}
