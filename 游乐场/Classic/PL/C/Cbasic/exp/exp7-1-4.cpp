#include<stdio.h>
#include<math.h>
int rec(int a[]){
	int n;
	scanf("%d",&n);
	for(int i=0;i<=n-1;i++){
		scanf("%d",&a[i]);
	}
	return n;
}
int check(int a1[],int a2[],int n1,int n2,int res[],int nres){
	for(int i=0;i<=n1-1;i++){
		int exist=0;
		for(int k=0;k<=n2-1;k++){
			if(a1[i]==a2[k]){
				exist=1;
				break;
			}
		}
		if(exist==0){
			nres=is(res,nres,a1[i]);
		}
	}	
	return nres;
}
int is(int res[],int nres,int num){
	if(nres==0){
		res[0]=num;
		nres++;
	}else{
		int j;
		for(j=0;j<=nres-1;j++){
			if(num==res[j]){
				break;
			}
		}
		if(j>nres-1){
			res[nres-1+1]=num;
			nres++;
		}
	}
	return nres;
}
int main(void){
	
	int a1[20],a2[20],n1,n2;
	n1=rec(a1);
	n2=rec(a2);
	int res[40],nres=0;
	nres=check(a1,a2,n1,n2,res,nres);
	nres=check(a2,a1,n2,n1,res,nres);
	
	for(int i=0;i<=nres-1;i++){
		if(i==0){
			printf("%d",res[i]);
		}else{
			printf(" %d",res[i]);
		}
	}
	
	return 0;
}

