#include <stdio.h>
#include<stdlib.h>
#include <assert.h>
#include <limits.h>
#include<string.h>
int sizeint=sizeof(int)<<3;
//1 2 4 8 16 32 64 128
int A(int x){//17=16+1
    int res=x+(x<<4);
    return res;
}
int B(int x){//-7=1-8
    int res=x-(x<<3);
    return res;
}
int C(int x){//60=64-4
    int res=(x<<6)-(x<<2);
    return res;
}
int D(int x){//-112=16-128
    int res=(x<<4)-(x<<7);
    return res;
}

int main(int argc, char* argv[]) {
    int x = 0x87654321;
    assert(A(x) == 17 * x);
    assert(B(x) == -7 * x);
    assert(C(x) == 60 * x);
    assert(D(x) == -112 * x);
    return 0;
}