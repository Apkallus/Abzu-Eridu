#include<stdio.h>
int ismatch(int number,int array[],int numarray);
int main(void){
	
	int m,n;
	int ma[20],na[20];
	scanf("%d",&m);
	for(int i=0;i<=m-1;i++){
		scanf("%d",&ma[i]);
	}
	scanf("%d",&n);
	for(int i=0;i<=n-1;i++){
		scanf("%d",&na[i]);
	}

	int res[40],count=0,resstate=0,flag;
	for(int i=0;i<=m-1;i++){
		flag=ismatch(ma[i],na,n);
		
		if(flag==0){
			if(resstate==0){
				res[count]=ma[i];
				resstate=1;
			}else{
				int isexist;
				isexist=ismatch(ma[i],res,count+1);

				if(isexist==0){
					count++;
					res[count]=ma[i];			
				}

			}
		}
	}
	
	for(int i=0;i<=n-1;i++){
		flag=ismatch(na[i],ma,m);
		
		if(flag==0){
			if(resstate==0){
				res[count]=na[i];
				resstate=1;
			}else{
				int isexist;
				isexist=ismatch(na[i],res,count+1);
				
				if(isexist==0){
					count++;
					res[count]=na[i];			
				}

			}
		}
	}
	
	
	for(int i=0;i<=count;i++){
		if(i==0){
			printf("%d",res[i]);
		}else{
			printf(" %d",res[i]);
		}

	}
	return 0;
}

int ismatch(int number,int array[],int numarray){
	int flag=0;
	for(int i=0;i<=numarray-1;i++){
			if(number==array[i]){
				flag=1;
				break;
			}
	}
	return flag;
}
