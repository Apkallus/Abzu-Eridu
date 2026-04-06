typedef enum {MODE_A,MODE_B,MODE_C,MODE_D,MODE_E} mode_t;

long switch3(long *p1,long *p2,mode_t action){
    long res=0,t;
    switch(action){
        //p1    p2  action
        //rdi   rsi edx
        case MODE_A:
            res=*p2;
            *p2=*p1;
            break;
        case MODE_B:
            res=*p1+*p2;
            *p1=res;
            break;
        case MODE_C:
            *p1=59;
            res=*p2;
            break;
        case MODE_D:
            res=27;
            *p1=*p2;
            break;
        case MODE_E:
            res=27;
            break;
        default:
            res=12;
            break;
    }
    return res;
}