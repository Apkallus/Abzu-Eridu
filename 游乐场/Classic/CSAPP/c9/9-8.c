static void *find_fit(size_t asize){
/*
    首次适配搜索
    从初始heap_listp开始
    得到当前bp的分配信息与大小
    如果未分配且大小足够则返回指针
    否则到下一个块进行同样的检查
    如果达到尾则返回NULL
*/
    size_t alloc, size;

    void *bp=(void *)heap_listp;     //得到初始指针
    
   
    while((bp=NEXT_BLKP(bp))!=mem_brk){//只要不到尾部就继续循环
        //@循环条件也可设为size>0

        alloc = GET_ALLOC(HDRP(bp));    //得到分配信息
        size = GET_SIZE(HDRP(bp));
        if(!alloc&&size>=asize){
            return bp;  // 如果未分配且大小足够返回bp
        }

    }

    return NULL;//到达尾部返回NULL
}