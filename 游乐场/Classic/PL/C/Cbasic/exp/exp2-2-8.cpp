#include<stdio.h>
#include<math.h>
int main(void){
	

	int shhmm,ehhmm,shh,smm,ehh,emm,chh,cmm;
	scanf("%d%d",&shhmm,&ehhmm);
	shh=shhmm/100;
	smm=shhmm%100;
	ehh=ehhmm/100;
	emm=ehhmm%100;
	chh=ehh-shh;
	cmm=emm-smm;
	if(cmm<0){
		chh--;
		cmm=cmm+60;
	}
	printf("%02d:%02d",chh,cmm);
	
	return 0;
}
