#include <stdio.h>
#include <assert.h>
#include <inttypes.h>

int signed_high_prod(int x,int y){
    return ((int64_t)x*y)>>32;
}
unsigned unsigned_high_prod(unsigned x,unsigned y){
    unsigned sx=x>>31;
    unsigned sy=y>>31;
    unsigned res=signed_high_prod(x,y);
    res=res+sx*y+sy*x;
    return res;
}
unsigned another_unsigned_high_prod(unsigned x, unsigned y){
    return ((size_t)x*y)>>32;
}
int main(int argc, char* argv[]) {
    unsigned x = 0x12345678;
    unsigned y = 0xFFFFFFFF;
    assert(another_unsigned_high_prod(x, y) == unsigned_high_prod(x, y));
    return 0;
  }