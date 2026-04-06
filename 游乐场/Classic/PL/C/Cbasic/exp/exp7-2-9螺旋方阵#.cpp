#include<stdio.h>
#include<math.h>
int rightfuc(int a[][9],int n,int num,int row,int cals,int cale){
	for(int i=cals;i<=cale;i++){
//		printf("-> %d,%d=%d\n",row,i,num);
		a[row][i]=num;
		num++;
	}
	return num;
}
int leftfuc(int a[][9],int n,int num,int row,int cals,int cale){
	for(int i=cale;i>=cals;i--){
//		printf("<- %d,%d=%d\n",row,i,num);
		a[row][i]=num;
		num++;
	}
	return num;
}
int downfuc(int a[][9],int n,int num,int cal,int rows,int rowe){
	for(int i=rows;i<=rowe;i++){
//		printf("v %d,%d=%d\n",i,cal,num);
		a[i][cal]=num;
		num++;
	}
	return num;
}
int upfuc(int a[][9],int n,int num,int cal,int rows,int rowe){
	for(int i=rowe;i>=rows;i--){
//		printf("^ %d,%d=%d\n",i,cal,num);
		a[i][cal]=num;
		num++;
	}
	return num;
}
int main(void){
	
	int n,a[9][9];
	scanf("%d",&n);	
	int rows=0,rowe=n-1,cals=0,cale=n-1,num=1;
	
	
	while(num<=n*n){
		num=rightfuc(a,n,num,rows,cals,cale);rows++;
		num=downfuc(a,n,num,cale,rows,rowe);cale--;
		num=leftfuc(a,n,num,rowe,cals,cale);rowe--;
		num=upfuc(a,n,num,cals,rows,rowe);cals++;
	}
	
//	putchar('\n');
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			printf("%3d",a[i][k]);
		}
		putchar('\n');
	}
	
	return 0;
}
