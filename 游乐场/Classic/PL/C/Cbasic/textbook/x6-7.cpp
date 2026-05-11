#include<stdio.h>
int isnumber(char ch);
int isop(char ch);
int calculate(int res,int num,char op);
int main(void){
	
	/*累计数 旧符号 数 新符号*/
	char ch,op='\0',state='\0';
	int res=0,num,error=0;
	while((ch=getchar())!='='){
		if(isnumber(ch)){
			if(state=='o'||state=='\0'){
				state='n';
				num=ch-'0';
			}else{
				num=num*10+ch-'0';
			}
		}else if(isop(ch)){
			if(state=='n'){
				res=calculate(res,num,op);
			}	
			op=ch;
			state='o';
		}else{
			error=1;
			break;
		}
			
	}
	if(error!=1&&(op!='/'||num!=0)){
		printf("%d",calculate(res,num,op));
	}else{
		printf("ERROR");
	}

	
	return 0;
}


int isnumber(char ch){
	int res=0;
	if(ch>='0'&&ch<='9'){
		res=1;
	}
	return res;
}
int isop(char ch){
	int res=0;
	if(ch=='+'||ch=='-'||ch=='*'||ch=='/'){
		res=1;
	}
	return res;
}
int calculate(int res,int num,char op){
	switch(op){
		case'+':res=res+num;break;
		case'-':res=res-num;break;
		case'*':res=res*num;break;
		case'/':res=res/num;break;
		default:res=num;
	}
	return res;
}


/*

#include<stdio.h>
int main()
{
	int n,t,s=0,y;
	char ch;
	scanf("%d",&s);
    while((ch=getchar())!='='){
    	if(ch>='0'&&ch<='9'||ch=='+'||ch=='-'||ch=='*'||ch=='/')
    	switch(ch){
    		
    		case '+':
			scanf("%d",&n);
			s+=n;
			break;
			
    		case '-':
			scanf("%d",&n);
			s-=n;
			break;
			
    		case '*':
			scanf("%d",&n);
			s*=n;
			break;
			
    		case '/':
			scanf("%d",&n);
            if(n==0){
                printf("ERROR");
                return 0;
            }
			s/=n;
			break; 			 			
		}
        else{
            printf("ERROR");
            return 0;
        }

	    	
	}
    printf("%d",s);

    return 0;
}
/*
switch(ch){
    			case '0':y=0;break;
    			case '1':y=1;break;
    			case '2':y=2;break;
    			case '3':y=3;break;
    			case '4':y=4;break;
    			case '5':y=5;break;
    			case '6':y=6;break;
    			case '7':y=7;break;
    			case '8':y=8;break;
    			case '9':y=9;break;	
			}
*/




