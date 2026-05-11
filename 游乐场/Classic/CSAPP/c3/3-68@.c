#include<stdio.h>
#define A 0
#define B 0
typedef struct {
    int x[A][B];
    long y;
} str1;
typedef struct{
    char array[B];
    int t;
    short s[A];
    long u;
} str2;
void setVal(str1 *p, str2 *q){
    long v1=q->t;
    long v2=q->u;
    p->y=v1+v2;
}
/*  对齐时的数量至少使得后一个变量保持当前位置，否则后一个变量的位置向前移动
    由此确定A与B以及A*B的范围
    rax=*(rsi+8)    ->  q->t    8/1=8个未对齐char  5<=B<=8
    rax+=*(rsi+32)  ->  q->u    32-8-4=20 20/2=未对齐的10个short    7<=A<=10
    *(184+rdi)=rax  ->  p->y    184/4=未对齐的46个int 45<=A*B<=46
*/
int main(void){//B=5,A=9,res=45
    int i,k,res;
    for(i=5;i<=8;i++){
        for(k=7;k<=10;k++){
            res=i*k;
            if(res>=45&&res<=46){
                printf("B=%d,A=%d,res=%d\n",i,k,res);
            }
        }
    }
}