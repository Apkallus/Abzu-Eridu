#include<stdio.h>
#include<math.h>
#include<string.h>
int main(void){
		
	char str[80],ch;
	int i=0,is;

	while((ch=getchar())!='\n'){
		if(i==0){
			str[i]=ch;
			i++;
		}else{
			is=0;
			for(int k=0;k<=i;k++){
				if(str[k]==ch){
					is=1;
					break;
				}
			}
			if(is==0){
				str[i]=ch;
				i++;
			}
		}	
	}
	str[i]='\0';
	for(int k=1;k<=i-1;k++){
		for(int g=0;g<=i-1-k;g++){
			if(str[g]>str[g+1]){
				char temp=str[g];
				str[g]=str[g+1];
				str[g+1]=temp;
			}
		}
	}
	puts(str);
	return 0;
}
