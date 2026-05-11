#include<stdio.h>
#include<string.h>
void fsort(char *color[],int n);
/*
int main(void){
	int i;
	char *pcolor[]={"red ","blue ","yellow ","green ","black "};
	
	fsort(pcolor,5);
	for(i=0;i<5;i++){
		printf("%s",pcolor[i]);
	}
	return 0;
}


void fsort(char *color[],int n){
	int k,j;
	char *temp;
	for(k=1;k<=n-1;k++){
		for(j=0;j<=n-1-k;j++){
			if(strcmp(color[j],color[j+1])>0){
				temp=color[j];
				color[j]=color[j+1];
				color[j+1]=temp;
			}
		}
	}
}
*/
int main(void){
	int i;
	char *pcolor[]={"red ","blue ","yellow ","green ","black "};
	
	fsort(pcolor,5);
	for(i=0;i<5;i++){
		printf("%s",*(pcolor+i));
	}
	return 0;
}
void fsort(char *color[],int n){
	int k,j;
	char *temp;
	for(k=1;k<=n-1;k++){
		for(j=0;j<=n-1-k;j++){
			if(strcmp(*(color+j),*(color+j+1))>0){
				temp=*(color+j);
				*(color+j)=*(color+j+1);
				*(color+j+1)=temp;
			}
		}
	}
}
