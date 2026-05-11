#include<stdio.h>
#include<math.h>
#include<string.h>
struct info{
	char name[10];
	float jbgz;
	float fdgz;
	float zc;
};
int main(void){
	int n;
	scanf("%d",&n);
	
	struct info res;
	for(int i=1;i<=n;i++){
		scanf("%s%f%f%f",res.name,&res.jbgz,&res.fdgz,&res.zc);
		printf("%s %.2f\n",res.name,res.jbgz+res.fdgz-res.zc);
	}	
	
	return 0;
}
