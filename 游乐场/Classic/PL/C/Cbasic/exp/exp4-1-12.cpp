#include<stdio.h>
#include<math.h>
int rea(int num);
int reb(int num);

int main(void){
	
	int num,a,b,c,t,count=1;
	scanf("%d",&num);	
	c=num;
	do{
		a=rea(c);
		b=reb(a);
		c=a-b;
		printf("%d: %d - %d = %d\n",count,a,b,c);
		count++;
	}while(c!=495&&count!=7);
	
	
	return 0;
}
int rea(int num){
	int array[3]={num%10,num/10%10,num/100},wei=3;
	for(int i=1;i<=wei-1;i++){
		for(int k=0;k<=wei-1-i;k++){
			if(array[k]<array[k+1]){
				array[k]^=array[k+1]^=array[k]^=array[k+1];
			}
		}
	}
	return array[0]*100+array[1]*10+array[2];
}
int reb(int num){
	return num=num%10*100+num/10%10*10+num/100;
}
