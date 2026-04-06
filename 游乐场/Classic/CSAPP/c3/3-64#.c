#define R 7
#define S 5
#define T 13
long A[R][S][T];

long store_ele(long i, long j, long k, long *dest){
    *dest=A[j*13+i*65+k];
    return sizeof(A);
    // 3640/8=455个元素
    // 65/13=5  i=5j=65k
    // 13/1=13  j=13k
    // 455/65=7 i最大范围
}

/*

    i   j   k   dest
    rdi rsi rdx rcx

    res=13*j
    t=i<<6
    i=i+(i<<6)+13*j
    k=k+i+(i<<6)+13*j
    *dest=A[k]
    res=3640

*/