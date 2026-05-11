#include<stdio.h>
#include<math.h>
int main(void){
	
	int rnum,gtime,count=1,unum,flag=0;
	scanf("%d%d",&rnum,&gtime);	
	
	for(int i=1;i<=gtime;i++,count++){
		scanf("%d",&unum);
		if(unum<0){
			break;
		}
		if(unum==rnum){
			if(count==1){
				printf("Bingo!");
			}else if(count<=3){
				printf("Lucky You!");
			}else{
				printf("Good Guess!");
			}
			flag=1;
			break;
		}else if(unum>rnum){
			printf("Too big\n");
		}else{
			printf("Too small\n");
		}
	}
	if(flag==0){
		printf("Game Over");
	}
	return 0;
}
