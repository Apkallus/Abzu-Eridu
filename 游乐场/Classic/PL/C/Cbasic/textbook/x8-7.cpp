#include<stdio.h>
#include<string.h>
int main(void){
	
	char array[5][80];
	for(int i=0;i<=5-1;i++){
		scanf("%s",array[i]);
	}
	
	for(int i=0;i<=4;i++){
		int min=i;
		for(int k=i+1;k<=4;k++){
			if(strcmp(array[k],array[min])<0){
				min=k;
			}
		}
		char temp[80];
		strcpy(temp,array[min]);
		strcpy(array[min],array[i]);
		strcpy(array[i],temp);
	}
	
	printf("After sorted:\n");
	for(int i=0;i<=4;i++){
		puts(array[i]);
	} 
	
	return 0;
}
