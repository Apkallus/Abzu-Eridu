#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
		
	char str[80],ch;
	int i=0,count=0;

	while((ch=getchar())!='\n'){
		str[i]=ch;
		i++;
	}
	str[i]='\0';
	ch=getchar();
	for(int k=0;k<=i-1;k++){
		if(ch==str[k]){
			count++;
		}
	}	
	printf("%d",count);
	return 0;
}
