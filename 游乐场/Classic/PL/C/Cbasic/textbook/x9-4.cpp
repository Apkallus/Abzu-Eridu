#include<stdio.h>
struct bookprice{
	char name[31];
	double price;
};
int main(void){
	
	int n;
	scanf("%d",&n);
	getchar();
	struct bookprice min,max,item;
	for(int i=0;i<=n-1;i++){
		gets(item.name);
		scanf("%lf",&item.price);
		getchar();
		if(i==0){
			min=max=item;
		}else{
			if(min.price>item.price){
				min=item;
			}else if(max.price<item.price){
				max=item;
			}
		}
	}

	printf("%.2f, %s\n%.2f, %s",max.price,max.name,min.price,min.name);


	
	return 0;
}
