#include<stdio.h>
#include<stdlib.h>
#include<time.h>
int main(void){
	
	int pcnumber,n;
	scanf("%d%d",&pcnumber,&n);
	
	int usernumber,i,flag=0,count=0;
	
	for(i=1;i<=n;i++){
		scanf("%d",&usernumber);
		if(usernumber>=0){
			count++;
			if(usernumber>pcnumber){
				printf("Too big\n");
			}else if(usernumber<pcnumber){
				printf("Too small\n");
			}else{
				flag=1;
				break;
			}			
		}else{
			break;
		}

	}
	
	if(flag){
		if(count==1){
			printf("Bingo!");
		}else if(count<=3){
			printf("Lucky You!");
		}else{
			printf("Good Guess!");
		}
	}else{
		printf("Game Over");
	}
	
	return 0;
}
