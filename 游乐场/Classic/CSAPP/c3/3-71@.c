#include <stdio.h>
#include <string.h>
#define MAXLEN 3
int good_echo(void){
    char str[MAXLEN]={0};
    char *res; 
    int i,endflag=0;
    res=fgets(str,MAXLEN,stdin);
    while(res){
   		printf("%s",str);
    	for(i=0;i<MAXLEN;i++){
    		if(str[i]=='\n'){
    			endflag=1;
    			break;
			}
		}
		if(endflag){
			break;
		}
    	res=fgets(str,3,stdin);
	}
}
int main(void){

    good_echo();
    return 0;
}
