#include<stdio.h>
struct st{
	int n;
	struct st *next;
};
int main(void){
	struct st a[3]={5,&a[1],7,&a[2],9,NULL};
	struct st *p=a;
	printf("a=%x\n",a);
	printf("a=%x\n",&a);
	printf("p=%x\n",p);
	printf("p->next->n=%d\n",p->next->n);
	printf("(++p)->n=%d\n",(++p)->n);
	return 0;
}
