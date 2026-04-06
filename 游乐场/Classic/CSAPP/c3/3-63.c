long switch_prob(long x,long n){
    long res=x;
    switch (n){
        case 60://0
        case 62://2
            res=x*8;
            break;
        case 63:
            res=x>>3;
            break;
        case 64:
            res=(x<<4)-x;
            x=res;
        case 65:
            x=x*x;
        default:
            res=x+0x4b;
            break;
        }
    return res;
}
/*
    x rdi, n rsi
    n-=0x3c
    if(n>5){
        goto default;
    }
    goto *(0x4006f8+n*8);

case 0:
case 2:
    res=x*8;
    return;
case 3:
    res=x>>3;
    return;
case 4:
    res=(x<<4)-x;
    x=res;
case 5://fall though
    x=x*x;
    
default://fall though
    res=x+0x4b;
    return;
*/