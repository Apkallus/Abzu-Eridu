#include<stdio.h>
int main(void)
{
	char ch;
	int i,letter,bk,dig,other;
	letter=0;
	bk=0;
	dig=0;
	other=0;
	for(i=0;i<10;i++){
		ch=getchar();
		if((ch>='a'&&ch<='z')||(ch>='A'&&ch<='Z')){
			letter++;
		}else if(ch==' '||ch=='\n'){
            bk++;
        }else if((ch>='0'&&ch<='9')){
			dig++;
		}else{
			other++;
		}
	}
	printf("letter = %d, blank = %d, digit = %d, other = %d",letter,bk,dig,other);
	
	return 0;
}
