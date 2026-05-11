#include<stdio.h>
struct po{
	double x;
	double y;
};
int main(void){
	struct po a,b,res;
	scanf("%lf%lf%lf%lf",&a.x,&a.y,&b.x,&b.y);
	res.x=a.x+b.x;
	res.y=a.y+b.y;
	if(res.x<0&&res.x>-0.05){
		res.x=0;
	}
	if(res.y<0&&res.y>-0.05){
		res.y=0;
	}
	printf("(%.1lf, %.1lf)",res.x,res.y);
	return 0;
}

