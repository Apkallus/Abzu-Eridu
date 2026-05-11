#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

//显示字节表示应使用字符指针
typedef unsigned char* byte_point;
void show_bytes(byte_point start,size_t len){
	for(size_t i=0;i<len;i++){
		printf(" %.2x",start[i]);
	}
	putchar('\n');
}
void show_short(short x){
	show_bytes((byte_point)&x,sizeof(x));
}
void show_long(long x){
	show_bytes((byte_point)&x,sizeof(x));
}
void show_double(double x){
	show_bytes((byte_point)&x,sizeof(x));
}
int main(void){
	
	int val=328;
	printf("call show_short\n");
	show_short((short)val);

	printf("call show_short\n");
	show_long((long)val);

	printf("call show_short\n");
	show_double((double)val);

	return 0;
} 
