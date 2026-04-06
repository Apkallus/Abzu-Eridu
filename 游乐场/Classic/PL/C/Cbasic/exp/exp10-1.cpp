#include<stdio.h>
#include<math.h>
#include<string.h>
#define PI 3.141592654
void Ball(){
	printf("Please enter the radius:\n");
	double r;
	scanf("%lf",&r);
	printf("%.2lf\n",4.0/3.0*PI*r*r*r); 
}
void Cylinder(){
	printf("Please enter the radius and the height:\n");
	double r,h;
	scanf("%lf%lf",&r,&h);
	printf("%.2lf\n",PI*r*r*h); 
}
void Cone(){
	printf("Please enter the radius and the height:\n");
	double r,h;
	scanf("%lf%lf",&r,&h);
	printf("%.2lf\n",PI*r*r*h*1.0/3.0); 
}
int main(void){
	
	int choice;
	do{
		printf("1-Ball\n2-Cylinder\n3-Cone\nother-Exit\nPlease enter your command:\n");
		scanf("%d",&choice);
		switch(choice){
			case 1:
				Ball();
				break;
			case 2:
				Cylinder();
				break;
			case 3:
				Cone();
				break;
			default:
				choice=0;
				break;
		}
	}while(choice!=0);	
	return 0;
}
