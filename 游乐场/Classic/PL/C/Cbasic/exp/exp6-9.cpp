#include<stdio.h>
#include<math.h>
int main(void){
	
	int count=0;
	char ch,lch=0,bch=0;
	do{
		ch=getchar();
		if(ch==' '||ch=='\n'){
			if(lch==1){
				count++;
			}
			bch=1;
			lch=0;
		}else{
			lch=1;
			bch=0;
		}
	}while(ch!='\n');
	
	printf("%d",count);
	return 0;
}
