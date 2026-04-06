#include<stdio.h>
int main(void)
{
	int fahr,celsius;
	/*fahr=150;*/
	printf("enter fahr:");
	scanf("%d",&fahr);
	
	celsius=5*(fahr-32)/9;
	printf("%d",celsius);
	
	return 0;
}
