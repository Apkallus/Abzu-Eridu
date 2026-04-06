/*
    int *p, int x,  int y
    rdi     rsi     rdx

    # 错误 在cqto符号扩展后 rdx为y的符号扩展高位 而不是寄存器一开始的参数y本身
    # 无符号乘积时rdx存放截断乘积的高位，即低位乘积的溢出
    rax=rdx     res=y
    cqto    y符号位扩展到128位 rdx=yh rax=yl
    rcx=rsi     
    rcx>>=63    t=x>>63=xh     //取x的高位             
    rcx*=rax    t=t*res=xh*yl   //xh*yl
    rdx*=rsi    d=yh*xl
    rcx+=rdx    t=t+d=xh*yl+yh*xl

u*  rax=rax*rsi(low)    res=y*x(low)=yl*xl 
u*  rdx=rax*rsi(high)   d=yl*xl//yl*xl截断乘积的高位

    rdx+=rcx    d=d+t=截断乘积（溢出）的高位+xh*yl+yh*xl

    *rdi=rax        low=rax
    *(rdi+8)=rdx    high=rdx

    x=2^64*xh+xl
    y=2^64*yh+yl
    x*y=(2^64*xh+xl)*(2^64*yh+yl)
    =2^64*xh*2^64*yh + 2^64*xh*yl + 2^64*yh*xl + xl*yl
    =2^128*xh*yh + 2^64*xh*yl + 2^64*yh*xl + xl*yl
    =2^64(xh*yl + yh*xl) + xl*yl

*/