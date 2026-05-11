/*
loop:
    movl esi,ecx //ecx=n
    movl $1,edx //edx=1
    movl $0,eax //eax=0
    jmp .L2
.L3:
    movq rdi,r8 //r8=x
    andq rdx,r8 //r8=x&rdx
    orq r8,rax  //rax=rax|(x&rdx)
    salq cl,rdx //rdx<<=n
.L2:
    testq rdx,rdx   
    jne .L3         //if(rdx!=0) goto loop
    rep;ret 
*/
long loop(long x, int n){
    //x int rdi, n in esi
    int res=0;
    long mask;
    for(mask=1;mask!=0;mask<<=(n%64)){//位移不超过位长w 对应%cl的低位m位 即为2的幂次-1
        //4位 角标0~3(0~n-1) 最大数为2^4-1 即1~4(1~n)位能够表示的数
        res|=(x&mask);
    }
    
    return res;
}