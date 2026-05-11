static void place(void *bp, size_t asize){
/*
    将块放置在空闲块的起始位置
    当剩余部分的大小>=最小块大小时，进行分割
*/

    
    // 
    

    size_t size = GET_SIZE(HDRP(bp));
    //得当前块的大小
    size_t res = size-asize;
    if(res>=2*DSIZE){
        //如果剩余部分应当分割    
        PUT(HDRP(bp), PACK(asize,1));//更新头信息后即可到脚
        PUT(FTRP(bp), PACK(asize,1));

        void *next=NEXT_BLKP(bp);
        PUT(HDRP(next), PACK(size,0));//分割块是空闲块，使用位为0
        PUT(FTRP(next), PACK(size,0));    
    }else{
        //否则使用当前块大小全部覆盖
        PUT(HDRP(bp), PACK(size,1));
        PUT(FTRP(bp), PACK(size,1));
    }
}