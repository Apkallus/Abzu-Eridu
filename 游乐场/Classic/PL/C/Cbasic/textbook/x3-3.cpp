#include<stdio.h>
int main(void){
	
	double licheng,chefei;
	int dengdai;
	scanf("%lf%d",&licheng,&dengdai);
	
	if(licheng<=3){
		chefei=10;
	}else if(licheng<=10){
		chefei=10+(licheng-3)*2;
	}else{
		chefei=10+(10-3)*2+(licheng-10)*3;		
	}
	

	chefei=chefei+dengdai/5*2;
	
	printf("%.0f",chefei);
	
	return 0;
}
