#include<stdio.h>
#include<math.h>
void showgame(int a[8][8],int n){
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			putchar(a[i][k]);
			if(k!=n-1){
				putchar(' ');
			}
		}
		putchar('\n');
	}
}
int game(int a[8][8],int n,int matchsucces){
	int x1,y1,x2,y2,res;
	scanf("%d%d%d%d",&x1,&y1,&x2,&y2);
	if(a[x1-1][y1-1]==a[x2-1][y2-1]&&a[x1-1][y1-1]!='*'){
		a[x1-1][y1-1]=a[x2-1][y2-1]='*';
		if(matchsucces<n*n/2-1){
			showgame(a,n);
		}
		res=1;
	}else{
		printf("Uh-oh\n");
		res=0;
	}
	return res;
}

int main(void){
	
	int n,a[8][8];
	scanf("%d",&n);	
	n=2*n;
	for(int i=0;i<=n-1;i++){
		for(int k=0;k<=n-1;k++){
			getchar();
			a[i][k]=getchar();	
		}
	}

	int matchfail=0,matchsucces=0,res,k;
	scanf("%d",&k);
	for(int i=1;i<=k;i++){
		res=game(a,n,matchsucces);
		if(res==0){
			matchfail++;
			if(matchfail==3){
				printf("Game Over\n");
				break;
			}
		}else{
			matchsucces++;
			if(matchsucces==n*n/2){
				printf("Congratulations!");
				break;
			}
		}
	}
	return 0;
}
