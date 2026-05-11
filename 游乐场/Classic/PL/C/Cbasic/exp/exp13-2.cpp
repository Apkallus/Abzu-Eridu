#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
struct box{
	int id;
	char password[5];
};
void makeid(struct box *p,int n){
	for(int i=1;i<=n;i++,p++){
		p->id=i;
		p->password[0]=NULL;
	}
}
void creatpassword(struct box *p){
	int pswd;
	srand((unsigned)time(NULL));
	pswd=rand();
	int i;
	for(i=0;i<=4-1;i++){
		p->password[i]=pswd%10+'0';
		pswd/=10;
	}
	p->password[i]='\0';
}
void put(struct box *p,int n){
	int coin;
	printf("put coin\n");
	scanf("%d",&coin);
	if(coin==1){
		int i;
		for(i=0;i<=n-1;i++,p++){
			if(p->password[0]==NULL){
				creatpassword(p);
				printf("id:%d pswd:%s\n",p->id,p->password);
				break;
			}
		}
		if(i>n-1){
			printf("box full\n");
		}
	}
}
void out(struct box *p,int n){
	char pswd[5];
	printf("enter password\n");
	scanf("%s",&pswd);
	int i;
	for(i=0;i<=n-1;i++,p++){
		if(strcmp(p->password,pswd)==0){
			printf("id:%d号箱已打开\n",p->id);
			p->password[0]=NULL;
			break;
		}
	}
	if(i>n-1){
		printf("password not exits");
	}
}
int main(void){
	
	int n;
	printf("enter n number\n");
	scanf("%d",&n);	
	struct box abox[30];	
	makeid(abox,n);
	
	int choice;
	do{
		printf("1.投硬币 2.输入密码 0.退出:\n");
		scanf("%d",&choice);		
		switch(choice){
			case 1:
				put(abox,n);
				break;
			case 2:
				out(abox,n);
				break;
			default:
				break;
		}
	}while(choice!=0);

	
	return 0;
}
