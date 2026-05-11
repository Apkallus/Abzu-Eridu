#include<stdio.h>
#include<math.h>
int main(void){
	
	int res,num;
	char ch;
	
	scanf("%d",&res);
	do{				
		ch=getchar();	
		if(ch=='+'||ch=='-'||ch=='*'||ch=='/'){
			scanf("%d",&num);
			if(ch=='+'){
				res=res+num;
			}else if(ch=='-'){
				res=res-num;
			}else if(ch=='*'){
				res=res*num;
			}else{
				if(num!=0){
					res=res/num;	
				}else{
					printf("ERROR");
					break;
				}
			}
		}else if(ch=='='){
			break;
		}else{
			printf("ERROR");	
			break;
		}
	}while(1);
	
	if(ch=='='){
		printf("%d",res);
	}
	
	return 0;
}
