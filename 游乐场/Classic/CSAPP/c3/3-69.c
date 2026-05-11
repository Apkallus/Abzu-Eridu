#define CNT 7
typedef struct{
    int idx;
    long x[4];
} a_struct;

typedef struct{
    int first;
    a_struct a[CNT];
    int last;
} b_struct;

void test(long i, b_struct *bp){
    int n=bp->first+bp->last;
    a_struct *ap=&bp->a[i];
    ap->x[ap->idx]=n;
}
/*
    ecx=*(rsi+0x120)    bp->last    0x120=288字节 
                        288-4(first)-4(填充)=280字节 为CNT个a_struct结构大小 包含偏置
    ecx+=*(rsi)         bp->first
    rax=rsi+rdi*40      rsi+i*40        ap      40为一个a_struct结构的大小 280/40=7 CNT
    rdx=*(rax+8)        *(rsi+i*40+8)   ap->idx 8为int first与4字节的填充 288-8=280
                                    且idx在结构的前面 使用rdx寄存器于是类型为long
    rcx=ecx符号扩展      将int存入a_struct的x数组时符号扩展 表示x的元素为long                    
    *(rax+rdx*8+16)=rcx ap->x[ap->idx]  
    rdx*8 8为a_struct结构中x数组的元素大小 x为long数组
    16包含 8的int first与4字节的填充
    16-8=8 剩余的8为x数组前的变量大小   
    如果只有字段idx与x 8为idx的大小 包含偏置    
*/