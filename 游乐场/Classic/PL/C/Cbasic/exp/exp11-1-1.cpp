#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main(void){
	
	int n=0;
	char str[11],*pa[20],*temp;
	gets(str);
	while(str[0]!='#'){
		pa[n]=(char*)malloc(sizeof(char)*(strlen(str)+1));
		strcpy(pa[n],str);
		n++;
		gets(str);
	}
	for(int i=1;i<=n-1;i++){
		for(int k=0;k<=n-1-i;k++){
			if(strlen(pa[k])>strlen(pa[k+1])){
				temp=pa[k];
				pa[k]=pa[k+1];
				pa[k+1]=temp;
			}
		}
	}
	for(int i=0;i<=n-1;i++){
		printf("%s ",pa[i]);
	}
	
	return 0;
}
