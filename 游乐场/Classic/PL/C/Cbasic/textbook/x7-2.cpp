#include<stdio.h>
int main(void){
	
	int n;
	scanf("%d",&n);
	int tab[2][10]={
	{0,1,2,3,4,5,6,7,8,9},
	{0,0,0,0,0,0,0,0,0,0}
	};
	getchar();
	char ch;
	while((ch=getchar())!='\n'){
		if(ch>='0'&&ch<='9'){
			tab[1][ch-'0']++;
		}
	}
	
	int maxtime=tab[1][0];
	for(int i=0;i<=10-1;i++){
		if(tab[1][i]>maxtime){
			maxtime=tab[1][i];
		}
	}
	printf("%d:",maxtime);
	for(int i=0;i<=10-1;i++){
		if(tab[1][i]==maxtime){
			printf(" %d",tab[0][i]);
		}
	}
	
	
	
	return 0;
}
