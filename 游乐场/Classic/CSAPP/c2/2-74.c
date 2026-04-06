#include <stdio.h>
#include <assert.h>
#include <limits.h>
int sizeint=sizeof(int)<<3;
int tsub_ok(int x,int y){//如x-y不溢出，返回1
    int xs=(x>>(sizeint-1));
    int ys=(y>>(sizeint-1));
    int xys=(x+y>>(sizeint-1));
    //x>0 y>0 ok
    //x>0 y<0 xy<0 isposvoer
    //x<0 y>0 xy>0 isnegover
    //x<0 y<0 ok

    int posover=~xs&ys&xys;
    int negover=xs&~ys&~xys;
    int res=1&~posover&~negover;

    return res;
}

int main(int argc, char* argv[]) {
    assert(!tsub_ok(0x00, INT_MIN));
    assert(tsub_ok(0x00, 0x00));
    return 0;
}