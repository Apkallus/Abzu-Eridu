union ele{
    struct{
        long *p;
        long y;
    } e1;
    struct{
        long x;
        union ele *next;
    } e2;
};
void proc(union ele *up){
//    up->__=*(__)-__;
    up->e2.x = *(up->e2.next->e1.p) - up->e2.next->e1.y;
}
/*
e1
p y
0 8
e2
x next
0 8

    rax=*(rdi+8)    rax为ele指针     ele +8处的指针 up->e2.next
    rdx=*(rax)      rdx为long指针    ele +0处的指针 up->e2.next->e1.p
    rdx=*(rdx)      rdx为long        *(up->e2.next->e1.p)
    rdx-=*(rax+8)   *(rax+8)为long   ele +8处的long up->e2.next->e1.y
                    *(up->e2.next->e1.p) - up->e2.next->e1.y
    *(rdi)=rdx      存入long ele +0处的long     up->e2.x 
                    up->e2.x = *(up->e2.next->e1.p) - up->e2.next->e1.y
*/