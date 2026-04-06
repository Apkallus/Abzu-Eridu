#include<stdio.h>
#include<math.h>
int main(void){
	
	int letter=0,blank=0,digit=0,other=0;
	char ch;
	for(int i=1;i<=10;i++){
		ch=getchar();
		if(ch>='0'&&ch<='9'){
			digit++;
		}else if(ch>='a'&&ch<='z'||ch>='A'&&ch<='Z'){
			letter++;
		}else if(ch=='\n'||ch==' '){
			blank++;
		}else{
			other++;
		}
	}	
	printf("letter = %d, blank = %d, digit = %d, other = %d",letter,blank,digit,other);
	
	return 0;
}
