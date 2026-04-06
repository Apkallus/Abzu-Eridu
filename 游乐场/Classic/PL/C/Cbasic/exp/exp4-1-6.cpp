#include<stdio.h>
#include<math.h>
int main(void){
	
	int n;
	scanf("%d",&n);	
	
	double fenzi=2,fenmu=1,lastfenzi,sum=0,item;
	for(int i=1;i<=n;i++){
		item=fenzi/fenmu;
		sum+=item;
		lastfenzi=fenzi;
		fenzi=fenzi+fenmu;
		fenmu=lastfenzi;
	}
	printf("%.2lf",sum);
	
	
	return 0;
}
