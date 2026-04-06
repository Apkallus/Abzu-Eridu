#include<stdio.h>
int main(void){
	
	int year,month,day;
	scanf("%d/%d/%d",&year,&month,&day);
	
	int tab[2][13]={
	{0,31,28,31,30,31,30,31,31,30,31,30,31},
	{0,31,29,31,30,31,30,31,31,30,31,30,31}};
	
	int leap=(year%4==0&&year%100!=0||year%400==0);
	
	for(int i=1;i<=month-1;i++){
		day=day+tab[leap][i];	
	}
	printf("%d",day);
	
	return 0;
}
