#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
#include<math.h>
typedef unsigned char* byte_point;

int k=15,n=63;
int sizeint=sizeof(int)<<3;
//字长80 
//符号1 阶码k=15 整数位1 小数位n=63
//假设与IEEE标准的不同只在于将隐藏的单独分配了位
//Bias=pow(2,k-1)-1
/*最小正非规格
    0 000 0 001
    M=f= pow(2,-n)
    E= 1-Bias= -pow(2,k-1)+2
    V= M*pow(2,E)
*/
long double minpn(void){
    size_t M=pow(2,-n);
    size_t Bias=pow(2,k-1)-1;
    size_t E=1-Bias;
    long double V=M*(pow(2,E));

    printf("%x\n",V);
    return V;
}

/*最小正规格
    0 001 1 000
    M=f+1=0+1
    e= 1
    E= e-Bias= -pow(2,k-1)+2
    V= M*pow(2,E)
*/
long double minpr(void){
    size_t M=1;
    size_t Bias=pow(2,k-1)-1;
    size_t E=1-Bias;
    long double V=M*pow(2,E);

    printf("%x\n",V);
    return V;
}
/*最大规格
    0 110 1 111
    M=f+1=1-pow(2,-n)+1
    e= pow(2,k)-2
    E= e-Bias= pow(2,k-1)-1
    V= M*pow(2,E)
*/
long double maxpn(void){
    size_t M=1-pow(2,-n)+1;
    size_t Bias=pow(2,k-1)-1;
    size_t e=pow(2,k)-2;
    size_t E=e-Bias;
    long double V=M*pow(2,E);
    
    printf("%x\n",V);
    return V;
}

/*无法产生与输出
void show_bytes(byte_point p,size_t size){
    for(size_t i=0;i<size;i++){
        printf("%.2x",p[i]);
    }
    putchar('\n');
}


int main(void){

    long double res;
    res=minpn();
    show_bytes((byte_point)&res,sizeof(res));
    res=minpr();
    show_bytes((byte_point)&res,sizeof(res));
    res=maxpn();
    show_bytes((byte_point)&res,sizeof(res));

    return 0;
}
*/