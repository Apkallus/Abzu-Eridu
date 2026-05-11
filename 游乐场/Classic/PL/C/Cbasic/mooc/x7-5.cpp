#include<stdio.h>
#include<math.h>
int rowmax(int n,int a[n][n],int row,int num){
	int res=1,i;
	for(i=0;i<=n-1;i++){
		if(a[row][i]>num){
			res=0;
			break;
		}
	}
	return res;
}
int colmin(int n,int a[n][n],int col,int num){
	int res=1,i;
	for(i=0;i<=n-1;i++){
		if(a[i][col]<num){
			res=0;
			break;
		}
	}
	return res;
}
int main(void){
	
	int n,num,flag=0;
	scanf("%d",&n);
	int array[n][n],row,col;
	for(row=0;row<=n-1;row++){
		for(col=0;col<=n-1;col++){
			scanf("%d",&num);
			array[row][col]=num;
		}
	}
	
	for(row=0;row<=n-1;row++){
		for(col=0;col<=n-1;col++){
			if(rowmax(n,array,row,array[row][col])&&colmin(n,array,col,array[row][col])){
				flag=1;
				printf("%d %d\n",row,col);
				break;
			}
		}
	}
	if(flag==0){
		printf("NONE");
	}

	return 0;
}