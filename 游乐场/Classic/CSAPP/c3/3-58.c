// rdi rsi rdx rcx
long decode2(long x,long y,long z){
    long t,res;
    t=x*(y-z);
    res=y<<63>>63;
    res=res^t;
}