#include<stdio.h>
int main(void){
	
	int fahr,lower,upper;
	double celsius;
	
	printf("Enter lower:");
	scanf("%d",&lower);
	printf("Enter upper:");
	scanf("%d",&upper);
	printf("fahr celsius\n");
	
//	for(fahr=lower,fahr<=upper,fahr++){
	for(fahr=lower;fahr<=upper;fahr+=2){
//		celsius=5/9*(fahr-32.0);
		celsius=5.0/9*(fahr-32);
//		printf("%3.0f%6.1f\n",fahr,celsius);
		printf("%3.0d%6.1f\n",fahr,celsius);
	}
	
	return 0;
}
