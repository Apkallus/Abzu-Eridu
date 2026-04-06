/*
    n   A   j
    rdi rsi rdx

    r8=n*4+1
    rdi=n*3

    if(n*3>0){
        r8<<=3 =(n*4+1)*8
        rcx=A+j*8
        eax=0
        edx=0

        do{
            rax+=*rcx   rcx->A[i][j]
            rdx+=1      rdx->j
            rcx+=r8     r8->数组步长 此时为数组列最大元素  NC=(n*4+1)*8/8=n*4+1
        }while(rdx!=rdi) j!=n*3     NR=n*3

    }else{
        eax=0       
    }
    

*/