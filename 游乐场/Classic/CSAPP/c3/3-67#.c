typedef struct{
    long a[2];
    long *p;
} strA;

typedef struct{
    long u[2];
    long q;
} strB;

strB process(strA s){
    strB r;
    r.u[0]=s.a[1];
    r.u[1]=s.a[0];
    r.q=*s.p;
    return r;
}
long eval(long x, long y, long z){
    strA s;;
    s.a[0]=x;
    s.a[1]=y;
    s.p=&z;
    strB r=process(s);
    return r.u[0]+r.u[1]+r.q;
}
/*
eval:
    //x   y   z
    //rdi rsi rdx
    rsp-=104 栈分配104字节
    *(rsp+24)=rdx   +24处存放z
    rax=rsp+24      rax得到+24的指针
    *(rsp)=rdi      +0处存放x
    *(rsp+8)=rsi    +8处存放y
    *(rsp+16)=rax   +16处存放+24的指针
    rdi=rsp+64      rdi参数1得到+64的指针
    call process
    rax=*(rsp+72)   rax得到+72处的值
    rax+=*(rsp+64)  再加+64处的值
    rax+=*(rsp+80)  再加+80处的值
80  z
72  x
64  y
    ...
24  z
16  &z
8   y
0   x
process://  被调用时主调函数压入返回地址 此时rsp-8 使用rsp偏移时-8
    //rdi=rsp+64 作为参数，调用前的rsp位置
    rax=rdi     rax得到+64的指针
    rdx=*(rsp+24)   rdx得到+24-8处保存的指针 ->指向z的指针
    rdx=*rdx        rdx得到此指针所指的值 ->z
    rcx=*(rsp+16)   rcx得到+16-8处的值  ->y
    *(rdi)=rcx      +64处存放y
    rcx=*(rsp+8)    rcx得到+8-8处的值 ->x
    *(rdi+8)=rcx    +72处存放x
    *(rdi+16)=rdx   +80处存放z
    在c程序中 传递参数为s的地址
    而在汇编中 传递参数为r在eval的地址 process引用s的值时使用rsp偏移

    在c程序中 process中定义的结构r不存在于汇编中
    它使用汇编在eval中分配的r的空间
    在函数返回结构时
    汇编在主调函数分配空间后,在被调函数中对分配空间进行操作
    相当于传递主调函数中定义的结构地址到被调函数

*/
