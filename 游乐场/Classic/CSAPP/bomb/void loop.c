// num=input1 a=0 b=14
int func4(int num,int b,int c){
    int expr,res;
    expr=(c-b)/2+b;
    //2*expr=c-b+2b
    //2*expr=c+b
    //expr=(c+b)/2 expr为c与b的平均值
    if(expr>num){
        c=expr-1;//如果平均值高于num则c等于平均值-1
        res=func4(num,b,c)*2;
    }else{//expr<=num
        if(expr>=num){  //<=与>= 实际条件为==
            res=0;      //如果expr==num返回0
        }else{       //expr<num
            b=expr+1;//如果平均值低于num则b等于平均值+1
            res=func4(num,b,c)*2+1;
        }
    }
    return res;
}


void phase_6(void){
    int array[21]; //rsp
    int *ap13=array;//r13
    int *rsi=array;
    int *r14=array;
    int count12=0;//r12
    int *bp,res,b;

    do{//数组元素0~5应当<=2 且值不相同
        //count12 0~5
        bp=ap13;    //bp=本轮数组元素地址 0~5
        res=*ap13-1;//res=数组元素值-1
        if(res>5){  //每轮元素应当1<=valval<=6
            // res>5
            //*ap13-1>5
            //*ap13>6
            //boom
            //jbe 无符号比较, -1后为负数时引爆
        }
        count12++;
        if(count12==6){//外循环变量到6退出循环 0~5有效
            break;
        }
        
        b=count12;//b=count12 1~5
        do{
            res=b;
            res=array[res];//b~5
        
            if(*bp==res){//遍历检查数组元素与其余元素的值是否相同
                //boom 如果相同
            }
        
            b++;            
            //第一次退出内循环时 b=6 ap13偏移6
        }while(b<=5);

        ap13++;//+int 到下一个数组元素
    }while(1);
//
//
    int *sip=&array[6];//rsi=rsp+24    第六个元素偏移地址
    int *ap=array;// rax=r14=rsp    初始地址
    int c=7;//ecx
    int d;//edx

    do{
        d=c-*ap;//7-标号0~5元素值
        *ap=d;  //存回
        ap++;//数组地址+
    }while(ap!=sip);//0~5元素地址 6退出循环
//
//
/*  使用常规语句取代goto语句 
    int s=0;//角标初始为0
    int *dp;//rdx
    goto L5;
L8://元素c>1
    dp=dp[1];//rdx=*(rdx+8) dp得到本身后一个地址
    res++;
    if(res!=c){
        goto L8;//只要循环条件!=元素就一直循环
    }else{
        goto L9;//不同在于此时dp为0x6032d0后面的一个地址
    }
L6://元素c<=1
    dp=0x6032d0;//edx获得一个固定地址
L9:
    array[s*2+8]=dp;//数组保存地址或long int  s 0~5
    //从角标8开始 递增2 8/10/12/14/16/18
    //保存地址或long int
    s++;
    if(s==6){
        goto L7;
    }
L5:
    c=array[s];
    if(c<=1){//如果元素<=1
        goto L6;
    }
    res=1;
    dp=0x6032d0;
    goto L8;//如果元素>1 则将跳到L8
L7:
*/


    int s=0;//角标初始为0
    int *dp;//rdx
    int *pa=array;//后半部分作为指针数组

    do{ //数组0~5元素值相对1的大小 
        //改变从rsp+32处写入的从0x6032d0开始的地址
        c=array[s];//取元素值
        dp=0x6032d0; //edx获得一个固定地址
        if(c>1){//如果元素值>1 则进入此段获得固定地址后面的指针
            res=1; 
            do{
                dp=*(dp+1);//rdx=*(rdx+8) dp得到本身后一个地址
                //指针指向数字
                //指针保存的值即数字地址+8得到下一个指针
                res++;
            }while(res!=c);//只要循环条件!=元素值就一直循环 
        }
        
        //如果元素c<=1 则dp地址为固定地址
        // *(rsp+rsi*2+32)=rdx
        //从rsp+32处开始将array作为指针数组
        pa[s+4]=dp;//指针数组保存地址  s 0~5
        //保存地址
        s++;// rsi+=4 一个int偏移
        if(s==6){//if(rsi==24) s作为int角标 0~5
            break;
        }
        
    }while(1);
//
//
    
    int *cp;
    int *bxp=pa[4];   //rbx=*(rsp+32) 保存的指针
    ap=&pa[5];  //rax=rsp+40 栈地址
    sip=&pa[10];//rsi=rsp+80 栈地址
    cp=bxp;      //rcx=rbx=*(rsp+32) 保存的指针

    do{//从pa[5]开始
        dp=*ap;//dp得到后一个指针
        *(cp+1)=dp;//*(rcx+8)=rdx 存入cp+偏移的位置
        //将后一个指针存入前一个指针对应数字+8处覆盖临近指针
        ap++;   //rax+=8 栈地址+
        if(ap==sip){//ap 5~9 10退出循环
            break;
        }
        cp=dp;//cp得到前一个指针
    }while(1);
    //循环存放5~9指针到4~8所指的偏移位置后
    //pa[9]的地址偏移处存放0
    *(dp+1)=0;  //*(rdx+8)=0
    
    
    b=5;        //ebp=5
    do{//*bxp=pa[4]    rbx=*(rsp+32)
        ap=*(bxp+1);   //rax=*(rbx+8) bxp[5~9]
        //ap得到当前指针所指地址+8处的临近指针
        res=*ap;     //eax=*rax 引用临近指针
        if(*bxp<res){//如果临近指针所指数字大于当前指针所指数字
            //boom
        }
        bxp=*(bxp+1);   //rbx=*(rbx+8)
        //bxp得到之前的临近指针
        b--;          //ebp--
    }while(b!=0);    //循环5次 1~5
}