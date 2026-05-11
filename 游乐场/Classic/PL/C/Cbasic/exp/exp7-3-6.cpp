#include<stdio.h>
#include<math.h>
int main(void){
	
	char ch;
	long int num=0,flag=1,first=1,m=0;
	while((ch=getchar())!='#'){
		if(ch=='-'){
			m=1;
		}
		if(ch>='0'&&ch<='9'||ch>='a'&&ch<='f'||ch>='A'&&ch<='F'){
			if(m&&first){
				flag=-1;
			}
			first=0;
			if(ch>='0'&&ch<='9'){
				num=num*16+ch-'0';
			}else if(ch>='a'&&ch<='f'){
				num=num*16+ch-'a'+10;
			}else if(ch>='A'&&ch<='F'){
				num=num*16+ch-'A'+10;
			}
		}
	}

	printf("%ld",flag*num);
		
	return 0;
}
