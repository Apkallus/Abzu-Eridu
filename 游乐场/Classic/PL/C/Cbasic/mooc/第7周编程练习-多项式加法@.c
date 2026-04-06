#include<stdio.h>
#define E 100
int main(void){
	
	int array[E+1],exp,base,countzero=0,first=1,i;
	memset(array,0,sizeof(array));
	
	while(countzero!=2){
		scanf("%d%d",&exp,&base);
		array[exp]+=base;
		if(!exp){
			countzero++;
		}
	}
	
	for(i=E;i>=0;i--){
		if(array[i]){
			if(array[i]>=0){
				if(!first){
					printf("+");
				}	
			}
			/*  if neg, already have '-' sign
			else{
				printf("-");
			}
			*/
			if(array[i]!=1&&array[i]!=-1){// when base==-1||1 not print base
				printf("%d",array[i]);
			}else if(array[i]==-1){// but when base==-1 print'-'
				printf("-");
			}
			if(i!=0){// when exp=0 not print x
				printf("x");
			}
			if(i>1){// when exp==-1||1 not print exp
				printf("%d",i);
			}
			first=0;
		}
	}
	if(first){// 0
		printf("0");
	}
	return 0;
}
