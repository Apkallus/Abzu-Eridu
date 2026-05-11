#include<stdio.h>
#include<stdlib.h>
#include<string.h>
struct flag{
	char ch;
	int is;
};
//不够满意 无法确定是否为最小 如果继续，传回单个奇数字符的数量，不到半数时普通移动，到半数时若其不在中间则从相反方向遍历 
//镜像移动同字符时从镜像角标向前找从远到近而不是从近到远
struct flag findodd(char *str,int len){
	int count,oddcount=0,already;
	struct flag res;
	char oddch[81];//保存是奇数的字符，在循环中排除 确保不重复计算
	memset(oddch,0,sizeof(oddch));
	res.is=0;
	for(int i=0;i<=len-1;i++){
		already=0;
		for(int g=0;g<oddcount;g++){
			if(oddch[g]==str[i]){
				already=1;
				break;
			}
		}
		if(already){
			continue;
		}
		count=0;
		for(int k=0;k<=len-1;k++){//遍历字符串，累计外循环字符的数量
			if(str[i]==str[k]){
				count++;
			}
		}
		if(count%2){//记录不是偶数字符的数量
			res.ch=str[i];
			oddch[oddcount]=str[i];
			oddcount++;
			printf("oddch=%c\n",res.ch);//如果最终是回文则可返回不是偶数的字符
		}
	}
	if(oddcount>1){//如果不是偶数的字符超过1个，则无法成为回文字符串
		res.is=1;
	}
	return res;
}

void sort(char *str,int len){
	struct flag res;
	int count=0,flagodd=0,lastcount=0;
	res=findodd(str,len);
	if(!res.is){//尝试将两个循环放在一起增加调试难度并且使得结构不清晰
		while(1){//无限循环确保奇数符号在中间
			for(int i=0;i<len-1;i++){
				for(int g=0;g<len-1;g++){//将奇数符号移动至中间
					if(str[g]==res.ch&&flagodd==0){//由于res结构初始化，如果是偶数长度则res.ch='\0' 应当设置条件使结构更清晰
						if(g!=(len-1)/2){
							char t=str[g];
							str[g]=str[g+1];
							str[g+1]=t;
							count++;
						}else{
							flagodd=1;
						}
					}
				}	
			}
			for(int i=0;i<len-1;i++){//将当前符号的下一个对应符号移动到镜像位置
				for(int k=i+1;k<len-1-i;k++){
					if(str[i]==str[k]&&str[i]!=str[len-1-i]){
						//str[i]!=str[len-1-i] 确保对称位置已经为当前字符时不交换
						char t=str[k];
						str[k]=str[k+1];
						str[k+1]=t;
						count++;
					} 
				}
			}
			if(str[(len-1)/2]!=res.ch){
				flagodd=0;
			}
			if(lastcount==count){
				break;
			}
			lastcount=count;
		}
		
		printf("%d	%s\n",count,str);
	}else{
		printf("Impossible\n");
	}
}
int main(void){
	
	int n;
	char str[80];
	strcpy(str,"a1b1ccab");
	sort(str,strlen(str));
	strcpy(str,"aabbcd");
	sort(str,strlen(str));

	return 0;
}
