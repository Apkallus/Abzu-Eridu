#include<stdio.h>
struct num{
	int fenzi;
	int fenmu;
	double res;
};
int main(void){
	struct num a,b;
	char ch;
	scanf("%d/%d %d/%d",&a.fenzi,&a.fenmu,&b.fenzi,&b.fenmu);
	a.res=1.0*a.fenzi/a.fenmu;
	b.res=1.0*b.fenzi/b.fenmu;
	if(a.res>b.res){
		ch='>';
	}else if(a.res<b.res){
		ch='<';
	}else{
		ch='=';
	}
	printf("%d/%d %c %d/%d",a.fenzi,a.fenmu,ch,b.fenzi,b.fenmu);
}
