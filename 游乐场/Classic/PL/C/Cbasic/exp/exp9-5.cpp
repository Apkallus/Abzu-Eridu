#include<stdio.h>
struct bo{
	char name[31];
	double price;
};
int main(void){

	struct bo book,max,min;
	int n;
	scanf("%d",&n);
	for(int i=0;i<=n-1;i++){
		getchar();
		gets(book.name);
		scanf("%lf",&book.price);
		if(i==0){
			max=min=book;
		}else{
			if(max.price<book.price){
				max=book;
			}
			if(min.price>book.price){
				min=book;
			}			
		}
	}

	printf("%.2lf, %s\n",max.price,max.name);
	printf("%.2lf, %s",min.price,min.name);		


	return 0;
}
