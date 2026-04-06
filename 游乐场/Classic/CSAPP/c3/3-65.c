/*
    do{
        rcx=*rdx    
        rsi=*rax    
        *rdx=rsi
        *rax=rcx
        rdx+=8      列  a[i][j]
        rax+=120    行  a[j][i]
    }while(rax!=rdi);

    120/8=15 M
*/