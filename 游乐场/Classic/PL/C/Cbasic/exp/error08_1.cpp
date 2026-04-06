#include<stdio.h>
int main(void){
	int max,x,y,*pmax,*px,*py;
	
	scanf("%d%d",&x,&y);
//	*px=&x;
//	*py=&y;
//	*pmax=&max;
	px=&x;
	py=&y;
	pmax=&max;
	*pmax=*px;
//	if(pmax<py){
	if(*pmax<*py){
		*pmax=*py;
	}
	printf("max=%d\n",max);
	
	return 0;
}

