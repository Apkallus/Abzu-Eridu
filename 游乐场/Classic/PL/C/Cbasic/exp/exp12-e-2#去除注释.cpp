#include<stdio.h>
#include<string.h>
#include<stdlib.h>
int main(void){
	
	FILE *fp1,*fp2;
	fp1=fopen("exp12-e-2f.cpp","r");
	fp2=fopen("exp12-e-2f.txt","w");
	
	char str[80],start[3]={"/*"},end[3]={"*/"},row[3]={"//"},t[3],ch;
	int sflag=0,eflag=0,rflag=0,dqmflag=0,perflag=0,sqmflag=0;
	
	while(fgets(str,80,fp1)!=NULL){
		if(str[0]=='#'){
			perflag=1;
		}else{
			perflag=0;
		}
		for(int i=0,n=strlen(str);i<=n-1;i++){
			int k;
			for(k=0;k<=1;k++){//×Ö·û´®×îºóÓÐÖÕÖ¹·û£¬»¹Î´³¬³ö·¶Î§ 
				t[k]=str[k+i];
			}
			t[k]='\0';
			
			if(t[0]=='\''&&dqmflag==0){
				sqmflag=sqmflag^1;
			}else if(t[0]=='"'&&sqmflag==0&&sflag==0&&rflag==0){
				dqmflag=dqmflag^1;
			}if(strcmp(t,start)==0&&(dqmflag==0||perflag==1)){
				sflag=1;
			}else if(strcmp(t,end)==0&&(dqmflag==0||perflag==1)){
				eflag=2;
				sflag=0;
			}else if(strcmp(t,row)==0&&dqmflag==0){
				rflag=1;
			}
			
			if(sflag){
				ch=' ';
			}else if(eflag){
				ch=' ';
				eflag--;
			}else if(rflag){
				ch=' ';
				if(i==n-1){
					rflag=0;
				}
			}else{
				ch=str[i];
			}				
			putchar(ch);
		}
		putchar('\n');
	}
	
	
	fclose(fp1);
	fclose(fp2);	
	
	return 0;
}
