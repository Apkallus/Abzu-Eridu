#include<stdio.h>
struct vv{
	double x,y;
};
int main(void){
	
	struct vv a,b,res;
	scanf("%lf%lf%lf%lf",&a.x,&a.y,&b.x,&b.y);
	res.x=a.x+b.x;
	res.y=a.y+b.y;
	if(res.x>-0.05&&res.x<0){
		res.x=0;
	} 
	if(res.y>-0.05&&res.y<0){
		res.y=0;
	}
	printf("(%.1f, %.1f)",res.x,res.y);

	
	
	return 0;
}
