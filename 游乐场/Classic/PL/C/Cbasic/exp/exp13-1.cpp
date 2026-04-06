#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define prdcnum 10
struct item{
	int id;
	char name[20];
	int price;
	int count;
};
struct item product[prdcnum]={{1,"Table-water",1},{2,"Table-water",1},{3,"Table-water",1},{4,"Coca-Cola",2},{5,"Mile",2},
			{6,"Beer",3},{7,"Orange-Juice",3},{8,"Sprite",3},{9,"Oolong-Tea",4},{10,"Green-Tea",4}};
int putmoney();
void selectitem(int money);
int main(void){

	int money;
	money=putmoney();
	if(money>0){
		selectitem(money);
	}
	
	return 0;
}
int putmoney(){
	int sum=0,money;
	printf("put money\n");
	scanf("%d",&money);
	while(money!=-1){
		sum=sum+money;
		scanf("%d",&money);
	}
	printf("total put money:%d\n",sum);
	return sum;
}
void selectitem(int money){
	int change=money,exitflag=0;
	int id;
	scanf("%d",&id);
	while(id!=-1&&!exitflag){
		int i;
		for(i=0;i<=prdcnum-1;i++){
			if(product[i].id==id){
				if(change-product[i].price>=0){
					change=change-product[i].price;
					product[i].count++;
					break;
				}else{
					printf("not enough change\n");
					exitflag=1;
					break;
				}
			}
		}
		if(i>9){
			printf("product not exist\n");
			exitflag=1;
			break;
		}
		if(exitflag==0){
			scanf("%d",&id);
		}
	}
	printf("Total:%dyuan,change:%dyuan\n",money,change);
	for(int i=0;i<=prdcnum-1;i++){
		if(product[i].count>0){
			printf("%s:%d;",product[i].name,product[i].count);
		}
	}
}
