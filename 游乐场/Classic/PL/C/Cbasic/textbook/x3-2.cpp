#include<stdio.h>
int main(void){
	
	int sp,lsp;
	scanf("%d%d",&sp,&lsp);
	
	double ov;
	if(sp>lsp){
		ov=1.0*(sp-lsp)/lsp*100;
		if(ov>=50){
			printf("Exceed %.0f%c. License Revoked",ov,'%');
		}else if(ov>=10){
			printf("Exceed %.0f%c. Ticket 200",ov,'%');			
		}else{
			printf("OK");
		}
	}else{
		printf("OK");
	}
	
	return 0;
}
