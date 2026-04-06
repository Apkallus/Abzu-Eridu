/*
 * mm-naive.c - The fasTEST, least memory-efficient malloc package.
 * 
 * In this naive approach, a block is allocated by simply incrementing
 * the brk pointer.  A block is pure payload. There are no headers or
 * footers.  Blocks are never coalesced or reused. Realloc is
 * implemented directly using mm_malloc and mm_free.
 *
 * NOTE TO STUDENTS: Replace this header comment with your own header
 * comment that gives a high level description of your solution.
 * 
 * 创建分离链表，从少量类别开始
 * 初始块 应该包含怎样的信息
 * （链表的类型）（链表首项的指针）
 * 
 * 
 * 已分配块只需头部
 * 未分配块包含头脚与前后向指针，于是在分配前应当更新链表
 * 
 * 指针的类型转换
 * 
 * 链表的指针指向bp还是对应的指针
 * 链表的指针指向bp，回忆结构链表，结构的指针指向下一个结构而不是下一个结构的指针
 * 
 * 对齐 初始头+块头后，bp地址应对齐
 * 
 * 可在分配新堆前检查结尾块的前一块是否分配以及大小，来减少新分配堆的大小
 * 
 * 由于头的后向指针保存在偏移位置，于是与NEXT_SLLP的后向指针为当前位置不冲突
 * 
 * ## 查看“错误”特别标注信息
 * 
 * 改善，设置专属于小块的池，头设置为池的大小，需记录池内块的数量，当全为空闲块时则free
    
    make clean; make   

    ./mdriver -a -V -f short1-bal.rep > trace
    ./mdriver -a -V -f short2-bal.rep > trace

    ./mdriver -a -V -f ./traces/amptjp-bal.rep > trace

    ./mdriver -a -V -f ./traces/random-bal.rep > trace
    超出内存范围

    ./mdriver -a -V -f ./traces/realloc-bal.rep > trace 
    ./mdriver -a -V -f ./traces/realloc2-bal.rep > trace 



    gdb --args ./mdriver -a -V -f short1-bal.rep
    break mm_init
    break mm_malloc
    break mm_free

    disas
        
    
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "ateam",
    /* First member's full name */
    "Harry Bovik",
    /* First member's email address */
    "bovik@cs.cmu.edu",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""
};


/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8
#define WSIZE 4
#define WSIZE_SHIFT 2
#define DSIZE 8
#define DSIZE_ALIGN 7
#define DSIZE_SHIFT 3
#define CHUNKSIZE  (1<<12)
#define SLLTYPE 13 //当前为每个类型一个链表头，需为奇数满足与结束块的对齐
#define MINBLOCKSIZE 16
#define MINBLOCKSIZE_SHIFT 4

#define TEST 0 //控制printf

#define MAX(x, y) ((x) > (y)? (x) : (y))  
#define MIN(x, y) ((x) < (y)? (x) : (y)) 

#define PACK(size, prev_alloc, alloc)  ((size) | (prev_alloc) | (alloc))
// 使用PACK的时候，应当提取出前一块的分配状态再与当前块大小与状态整合

#define GET(p)       (*(unsigned int *)(p))
#define GETPTR(p)       ((char *)*(unsigned int *)(p))
#define PUT(p, val)  (*(unsigned int *)(p) = (val))
#define PUTPTR(p, val)  (*(unsigned int *)(p) = (unsigned int)(val))
// 在当前指针位置读取或写入，应当移动到头/脚或前后向指针位置

#define GET_SIZE(p)  (GET(p) & ~0x7)               
#define GET_ALLOC(p) (GET(p) & 0x1)  
#define GET_PREV_ALLOC(p) (GET(p) & 0x2)
// 提取当前位置的状态信息，应当移动到头/脚或前后向指针位置
// # GET_PREV_ALLOC宏需要将bp移动到头，而实际直接使用了bp

#define HDRP(bp)       ((char *)(bp) - WSIZE)                      
#define FTRP(bp)       ((char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE) 
// 使用bp指针，头在bp前一个WSIZE的位置
// 使用FTRP前应当更新头信息
// 已分配无脚，未分配的脚在+当前块size-头脚的位置

#define NEXT_SLLP(bp)    ((char *)(bp)) 
#define PREV_SLLP(bp)    ((char *)(bp) + WSIZE)                     
// 移动到后向指针位置与前向指针位置
// 对于空闲块，bp位置与bp+WSIZE即为指针位置

#define NEXT_BLKP(bp)  ((char *)(bp) + GET_SIZE(((char *)(bp) - WSIZE))) 
#define PREV_BLKP(bp)  ((char *)(bp) - GET_SIZE(((char *)(bp) - DSIZE)))
// 到下一块得到本块大小后，在bp偏移
// 到上一块从上一块的脚得到其大小后，在bp偏移

#define SET_ALLOC_TO_NEXT(bp)  (*(unsigned int *)(HDRP(NEXT_BLKP(bp))) =(GET(HDRP(NEXT_BLKP(bp))))|0x2) 
#define CLEAN_ALLOC_TO_NEXT(bp)  (*(unsigned int *)(HDRP(NEXT_BLKP(bp))) =(GET(HDRP(NEXT_BLKP(bp))))&~0x2)  
//  |0x2设置 &~0x2清除

static char *heap_begin=0;
static char *heap_listp=0;

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~0x7)

#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))

// 函数声明
static void *extend_heap(size_t size);
static void place(void *bp, size_t asize);
static void place_realloc(void *bp, size_t asize, size_t csize);
static void *find_fit(size_t asize);
static void *coalesce(void *bp);
static void delete_sll(void *bp);
static void set_sll(void *bp, size_t size);
static int find_type(size_t size);
static int printblock(int i, void *bp); 
static void checkheap();
static void checkblock(void *bp);

// 根据size的大小寻找链表类型
static int find_type(size_t size){
    int index, end;
    size_t t = size>>MINBLOCKSIZE_SHIFT;
    //初始位移对应最小块大小的位移

    for(index=0, end=SLLTYPE-1; index<end && t; index++){
        //n个type n-1下标最大值， for循环后index为n，于是index<n-1则不超出
        t=t>>1;
    }

    if(TEST)
    printf("find_type size=%u,index=%d\n",size,index);
    
    return index;
}
// 寻找空闲块
// ##错误 之前只是在大小类型的首项检查是否匹配，而没有遍历链表
// 这导致即使在大小类型拥有匹配块，仍由于首项不匹配而进入下一个类型
// 在更改后，需同时将链表按大小排序，否则在同一类中，小块可能放到大块中
static void *find_fit(size_t asize){

    if(TEST)
    printf("into find_fit asize=%u\n",asize);

    void *bp, *tbp, *sllbp;
    char *begin=(char *)heap_begin;
    int index, find=0; 
    // ！！index初值设为-1来判断是否找到
    // #错误 之前设置index为size_t也就是无符号整型
    // 后续判断将永为真

    index=find_type(asize);
    for(int i=index; i<SLLTYPE && !find; i++){
        tbp=begin+i*WSIZE;
        sllbp=GETPTR(tbp);
        for(;sllbp && !find; sllbp=GETPTR(NEXT_SLLP(sllbp))){
            //只要不到链表尾且没找到就继续循环到下一类
            if(GET_SIZE(HDRP(sllbp))>=asize){
                // #错误 只检查了是否为空，而忽略了大小的检查
                // index=i;
                find=1;
                break;
            }
        }

    }
    
    if(find){
        // 如找到不为空的类型首项，则返回
        // 改为遍历类型链表
        bp=(void *)sllbp;

        // 并更新链表
        // set_sll(bp, asize);
        // #### 错误 只是找到，没有理由更新链表
        // set_sll在释放块到空闲块时使用，而find搭配malloc使用，本身即为空闲块
        // #### 此项导致了之前出现的，块的前后向指向本身
        // #### 当前块为首项时，此句将当前块的首尾指向本身
    }else{
        // 如index仍为-1，表示未找到则返回NULL
        bp=NULL;
    }

    if(TEST)
    printf("out find_fit bp=%p\n",bp);

    return bp;
}

/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    if(TEST)
    printf("into mm_init\n");


    //初始化时需分配分离链表的结构
    //目前设计 各类链表头只包含首项指针，之后可能需增加末项指针或链表块数量
    //初始为 分离链表种类+结束尾
    if((heap_begin = mem_sbrk((1+SLLTYPE)*WSIZE))==(void*)-1){
        //分配起始块
        return -1;
    }
    heap_listp = heap_begin;
    if(TEST)
    printf("##>>heap_begin %p\n", heap_begin);
    
    //各类链表头
    // 
    // PUT(heap_listp+1*WSIZE, 0);
    // PUT(heap_listp+2*WSIZE, 0);
    for(int i=0; i<SLLTYPE; i++){
        PUT(heap_listp+i*WSIZE, 0);
    }
    // 结束尾
    PUT(heap_listp + SLLTYPE * WSIZE, 0x1|0x2);

    heap_listp += ((SLLTYPE+1)*WSIZE); 
    // ## heap_listp应当从end的bp开始，即为结束块头的后面
    //由于此时不设置头部，于是放在尾的后面，这样新分配堆时将覆盖尾，然后创建新尾
    
    if(extend_heap(CHUNKSIZE)==NULL){
        return -1;
    }

    if(TEST){
        checkheap();
        printf("out mm_init\n"); 
    }
    return 0;
}

/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    if(TEST){
        printf("\n>>>>>> into mm_malloc size=%u\n", size);
        printf("mem_heapsize=%u\n",mem_heapsize());        
    }



    // int newsize = ALIGN(size + SIZE_T_SIZE);
    // void *p = mem_sbrk(newsize);
    // if (p == (void *)-1)
	// return NULL;
    // else {
    //     *(size_t *)p = size;
    //     return (void *)((char *)p + SIZE_T_SIZE);
    // }

    size_t asize;
    size_t extendsize;
    char *bp=NULL;

    if (heap_listp == 0){
        // 初始化
        mm_init();
    }
    if (size == 0){
        // 分配大小为0，返回NULL
        return NULL;        
    }
    if(TEST){
        printf("\n---------just mm_malloc---------\n");
        checkheap();     
        printf("---------end just mm_malloc---------\n");
    }
    
        // 对于空闲块 头/脚/前向指针/后向指针各4字节 最小16字节
        // 对于分配块 头+有效载荷 4+1对齐后8字节
        // 最小块大小为16字节
    if (size <= WSIZE+DSIZE){
        // 12以下直接对应最小块大小
        asize = MINBLOCKSIZE;
    }else{
        // 有效载荷+头 再对齐
        asize =((size +WSIZE + DSIZE_ALIGN) >>DSIZE_SHIFT) <<DSIZE_SHIFT;
    }

    if(TEST)
    printf("mm_malloc asize=%u\n", asize);

    if ((bp = find_fit(asize)) != NULL) {  
        // 如果找到匹配则分配后返回
        place(bp, asize); 

        if(TEST){
            printf("mm_malloc find_fit != NULL \n");
            checkheap();              
        }
               
        return bp;
    } 

    extendsize = MAX(asize,CHUNKSIZE); 
        // 取自定义大小与分配大小的大值
    if ((bp = extend_heap(extendsize)) != NULL) {
        // 如果无匹配则扩展堆后分配 
        place(bp, asize);  

        if(TEST){
            printf("mm_malloc extend_heap\n");
            checkheap();
        }

        return bp; 
    }
        
    if(TEST){
        printf(">>>>>> out mm_malloc bp=%p\n", bp);
        checkheap();        
    }

    return NULL;
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *ptr)
{
    if(TEST)
    printf("into mm_free ptr=%p\n", ptr);

    if (ptr == 0) {
        // 如果为NULL则返回
        return;
    }

    size_t size = GET_SIZE(HDRP(ptr));
    if (heap_listp == 0){
        // 如果调用free前未初始化则进行初始化
        // 是否必要？
        mm_init();
    }

    size_t prev_alloc = GET_PREV_ALLOC(HDRP(ptr));
    set_sll(ptr, size);
    PUT(HDRP(ptr), PACK(size, prev_alloc, 0));
    PUT(FTRP(ptr), PACK(size, prev_alloc, 0));
    // 添加到空闲链表中并更新信息

    CLEAN_ALLOC_TO_NEXT(ptr);
    // 在释放后清除后一块保存的分配位

    coalesce(ptr);
    // 立即合并

    // if(TEST){
    //     printf("out mm_free\n");
    //     checkheap();              
    // }
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{

    if (heap_listp == 0){
        // 初始化
        mm_init();
    }
    // checkheap();

    void *resptr=ptr;
    size_t old_size, res_size, align_size;

    if(!ptr){
        resptr=mm_malloc(size);
        return resptr;
    }
    if(!size){
        mm_free(resptr);
        return resptr;
    }
    
    //##错误 没有处理size小于最小块大小的情况，也忽略了此处的size不含头部大小
    //##简单分配新块的malloc拥有最小块判断，此处同样应当有
    if (size <= WSIZE+DSIZE){
        // 12以下直接对应最小块大小
        align_size = MINBLOCKSIZE;
    }else{
        // 有效载荷+头 再对齐
        align_size =((size +WSIZE + DSIZE_ALIGN) >>DSIZE_SHIFT) <<DSIZE_SHIFT;
    }

    //判断前后块是否未分配
    //若未分配则判断大小是否足够
    //若足够则更新信息
    //若不足够则调用malloc，将信息复制到新块后释放旧块

    // 可优化 #若本块为结束块之前的已分配块，若增加
    //#则新分配块的值为对齐后的目标大小-当前大小，再合并

    // 可优化 #若本块为结束块之前的未分配块再之前的已分配块
    //#则为对齐后的目标大小-当前大小-后面的未分配块大小

    //当前的合并空闲块函数中将更新头脚与设置新块的双向链表
    //直接调用将覆盖数据
    

    old_size = GET_SIZE(HDRP(ptr));
    //得到之前块的大小

    if(old_size==align_size){
        // case0 新旧大小相同，返回
        return resptr;
    }

    size_t prev_alloc = GET_PREV_ALLOC(HDRP(ptr));
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(ptr)));
    size_t next_size = GET_SIZE(HDRP(NEXT_BLKP(ptr)));

    if(old_size>align_size){
        // case1 缩小
        // 得到后一块的空闲状态与大小
        // 如为空闲块，合并块大小=将释放块的大小+后空闲块的大小
        // 如否，则只计算释放块的大小
        // 判断后面块的最终大小是否足够最小块大小
        // 如足够则更新信息，如不足则无法释放而无变化
        size_t diff_size = old_size - align_size;
        // 将释放块的大小
        size_t coalesce_size = diff_size + (next_alloc?0:next_size);

        // printf("diff_size=%u -> old_size=%u-align_size=%u,coalesce_size=%u\n"
        //     ,diff_size,old_size,align_size,coalesce_size);
        if(diff_size>=MINBLOCKSIZE){
            //示例测试未使用
            printf("----diff_size>=MINBLOCKSIZE\n");            
            // 如果将释放块的大小本身已足够
            // 在设置两个块的头部后即可调用free释放后块
            PUT(HDRP(ptr), PACK(align_size, prev_alloc, 1));

            //此时的NEXT_BLKP(ptr)为释放块bp
            PUT(HDRP(NEXT_BLKP(ptr)), PACK(diff_size, 0x2, 1));
            mm_free(NEXT_BLKP(ptr));    
            return ptr;

        }else if(!next_alloc){
            // printf("----!next_alloc && coalesce_size>=MINBLOCKSIZE\n"); 
            // 如果下一块未分配，而合并大小满足对齐且足够最小块
            // # 由于未分配块一定满足最小块，于是无需检查此条件
            // # 满足未分配即可合并
            // printf("diff_size=%d,next_size=%d,coalesce_size=%d\n"
            //     ,diff_size,next_size,coalesce_size);

            // printblock(1,ptr);
            // printblock(2,NEXT_BLKP(ptr));

            delete_sll(NEXT_BLKP(ptr));
            //此时的NEXT_BLKP(ptr)为下一块bp
            //将下一块从空闲链表中删除

            PUT(HDRP(ptr), PACK(align_size, prev_alloc, 1));
            PUT(HDRP(NEXT_BLKP(ptr)), PACK(coalesce_size, 0x2, 1));
            //此时的NEXT_BLKP(ptr)为释放块bp
            mm_free(NEXT_BLKP(ptr));   
            // printblock(1,ptr); 
            // printblock(2,NEXT_BLKP(ptr));
            return ptr;
        }else{
            //如果分离块不足最小块且后一块为已分配
            //直接返回
            return ptr;
        }
    }

    if(old_size<align_size){
        //case2 增加
        // 查看前后块的状态与大小
        // 如足够则合并复制
        // 如不足则分配新块
        size_t prev_size = 0;
        if(!prev_alloc){
            prev_size=GET_SIZE(HDRP(PREV_BLKP(ptr)));
        }
        size_t coalesce_size = old_size+(next_alloc?0:next_size)+prev_size;
        // coalesce_size当前为两块合计

        // ########
        // 从memcpy改为自定义字符复制函数后再改为memmove后通过
        // ########
        if(coalesce_size>=align_size){
            // 如果合并块后大小满足，则进行合并复制
            // printf("coalesce_size=%u align_size=%u\n",coalesce_size,align_size);

            // if(!prev_alloc)
            // printblock(1,PREV_BLKP(ptr));
            // printblock(2,ptr);
            // printblock(3,NEXT_BLKP(ptr));

            char *next_bp=NEXT_BLKP(ptr);
            char *prev_bp=NULL;
            if(!prev_alloc)
                prev_bp=PREV_BLKP(ptr); 

            if (prev_alloc && !next_alloc) { 
                //无需复制
                // printf("prev_alloc && !next_alloc\n");
                delete_sll(next_bp);
                
                place_realloc(ptr, align_size, coalesce_size);

            }else if (!prev_alloc && next_alloc) { 
                // printf("!prev_alloc && next_alloc\n");

                delete_sll(prev_bp);

                memmove(prev_bp, ptr, old_size-WSIZE);
                
                place_realloc(prev_bp, align_size, coalesce_size);
                ptr = prev_bp;

            }else {     
                // printf("!prev_alloc && !next_alloc\n");
                // ###
                // 使用memmove可，使用memcpy不可
                // 其他方法是，尝试改变复制的方向
                // 以及malloc一个缓冲区，使用缓冲区复制后再free 
                // ###
                delete_sll(next_bp);    
                delete_sll(prev_bp);

                // checkstr(ptr, old_size-WSIZE);
                memmove(prev_bp, ptr, old_size-WSIZE);
                // checkstr(prev_bp, old_size-WSIZE);

                place_realloc(prev_bp, align_size, coalesce_size);  
                // checkstr(prev_bp, old_size-WSIZE);

                ptr = prev_bp;
            }

            // if(!GET_PREV_ALLOC(HDRP(ptr)))
            // printblock(1,PREV_BLKP(ptr));            
            // printblock(2,ptr);
            // printblock(3,NEXT_BLKP(ptr));            

            return ptr;

        }else{
            // 合并大小仍不满足，分配新块
            //  可优化，将前面的合并大小判断内容作为函数，实现上述对后两块的空闲检查
            // 如符合则分配空间后调用函数并返回，否则继续此分支
            resptr = mm_malloc(size);
            if(resptr != NULL){
                //若没有分配到块则返回NULL
                //若分配到块则复制
                // res_size = GET_SIZE(HDRP(resptr));
                // 最开始只实现了新分配堆，现在实现了其他分支后可将内容注释

                memmove(resptr, ptr, old_size-WSIZE);
                // memmove(resptr, ptr, MIN(res_size-WSIZE, old_size-WSIZE));
                // 新块与旧块的较小值为最终复制大小
                // 原大小-头WSIZE的大小为复制大小
                mm_free(ptr);
                // 此处指针位置与内容不重叠
                // 于是mm_free与复制不冲突
                // 若改为合并，需处理可能的冲突
            }
            return resptr;
        }


    }
    return ptr;
}
    

    

// 扩展堆
static void *extend_heap(size_t size){
    if(TEST)
    printf("into extend_heap size=%u\n",size);

    char *bp;
    size = ALIGN(size);
    //此处的对齐是否必要
    
    if((long)(bp = mem_sbrk(size)) == -1){
        //调用mem_sbrk分配空间
        return NULL;
    }

    size_t prev_alloc = GET_PREV_ALLOC(HDRP(bp));
    PUT(HDRP(bp), PACK(size, prev_alloc, 0));
    PUT(FTRP(bp), PACK(size, prev_alloc, 0));
    set_sll(bp, size);
    //新块的头覆盖旧堆结束块
    //coalesce也有set_sll，可简化
    PUT(HDRP(NEXT_BLKP(bp)), PACK(0, 0, 1));
    //设置新的堆结束块

    if(TEST)
    printf("out extend_heap\n");

    return coalesce(bp);
}

//按地址排序 内存利用率反而下降
static void address_set_sll(void *bp, size_t size){

    if(TEST)
    printf("into set_sll bp=%p size=%u\n", bp, size);
    //函数或宏
    //将块放到size对应的链表中
    //暂时将新空闲块作为首项
    //之后探索按地址排列
    //或许只是增加尾项，简单的比较再从前或后搜索
    //将当前块的后向块设置为容量链表的首项
    //再将容量链表的首项设置为当前块

    int index=find_type(size);
    //index得到匹配类型的头部偏移
    char *ctbp=(char *)bp;

    char *sll_type_ptr = heap_begin+index*WSIZE;
    //heap_begin的void指针转为char指针后偏移
    char *sll_oldfirst = GETPTR(sll_type_ptr);
    //偏移后作为无符号整型读取数据作为地址

    char *sll_loop_prev = sll_type_ptr;
    char *sll_loop_next = GETPTR(NEXT_SLLP(sll_loop_prev));

    while(sll_loop_next && sll_loop_next<ctbp){
        sll_loop_prev = sll_loop_next;
        sll_loop_next = GETPTR(NEXT_SLLP(sll_loop_next));
    }
    
    if(TEST)
    printf("    set_sll sll_type_ptr=[%d]%p sll_oldfirst=%p\n",index,sll_type_ptr,sll_oldfirst);

    PUTPTR(NEXT_SLLP(bp), sll_loop_next);
    //新增空闲块的后向设置为分离类型链表的首项

    PUTPTR(PREV_SLLP(bp), sll_loop_prev);
    //新增空闲块的前向设置为分离类型头

    PUTPTR(sll_loop_prev, bp);
    //设置新增空闲块为链表首项

    // #错误 未对首项是否为NULL进行条件检测，导致段错误
    if(sll_loop_next){
        PUTPTR(PREV_SLLP(sll_loop_next), bp);
        // #错误，直接将指针保存在下一项的bp而不是前向指针处
        // 如不为NULL 将之前的首项块前向设置为当前块
    }

    if(TEST)
    printf("out set_sll\n");
}

//应当按大小排序
static void set_sll(void *bp, size_t size){

    if(TEST)
    printf("into set_sll bp=%p size=%u\n", bp, size);
    //函数或宏
    //将块放到size对应的链表中
    //暂时将新空闲块作为首项
    //之后探索按地址排列
    //或许只是增加尾项，简单的比较再从前或后搜索
    //将当前块的后向块设置为容量链表的首项
    //再将容量链表的首项设置为当前块

    int index=find_type(size);
    //index得到匹配类型的头部偏移

    char *sll_type_ptr = heap_begin+index*WSIZE;
    //heap_begin的void指针转为char指针后偏移
    //偏移后作为无符号整型读取数据作为地址

    char *sll_loop_prev = sll_type_ptr;
    char *sll_loop_next = GETPTR(NEXT_SLLP(sll_loop_prev));
    
    while(sll_loop_next && GET_SIZE(sll_loop_next)<size){
        sll_loop_prev = sll_loop_next;
        sll_loop_next = GETPTR(NEXT_SLLP(sll_loop_next));
    }


    PUTPTR(NEXT_SLLP(bp), sll_loop_next);
    //后向设置

    PUTPTR(PREV_SLLP(bp), sll_loop_prev);
    //前向设置

    PUTPTR(sll_loop_prev, bp);
    //更新前节点

    // #错误 未对首项是否为NULL进行条件检测，导致段错误
    if(sll_loop_next){
        PUTPTR(PREV_SLLP(sll_loop_next), bp);
        // #错误，直接将指针保存在下一项的bp而不是前向指针处
        // 后节点如不为NULL 更新后节点
    }

    if(TEST)
    printf("out set_sll\n");
}

//成为首项排序
static void sx_set_sll(void *bp, size_t size){

    if(TEST)
    printf("into set_sll bp=%p size=%u\n", bp, size);
    //函数或宏
    //将块放到size对应的链表中
    //暂时将新空闲块作为首项
    //之后探索按地址排列
    //或许只是增加尾项，简单的比较再从前或后搜索
    //将当前块的后向块设置为容量链表的首项
    //再将容量链表的首项设置为当前块

    int index=find_type(size);
    //index得到匹配类型的头部偏移

    char *sll_type_ptr = heap_begin+index*WSIZE;
    //heap_begin的void指针转为char指针后偏移
    char *sll_oldfirst = GETPTR(sll_type_ptr);
    //偏移后作为无符号整型读取数据作为地址
    
    if(TEST)
    printf("    set_sll sll_type_ptr=[%d]%p sll_oldfirst=%p\n",index,sll_type_ptr,sll_oldfirst);

    PUTPTR(NEXT_SLLP(bp), sll_oldfirst);
    //新增空闲块的后向设置为分离类型链表的首项

    PUTPTR(PREV_SLLP(bp), sll_type_ptr);
    //新增空闲块的前向设置为分离类型头

    PUTPTR(sll_type_ptr, bp);
    //设置新增空闲块为链表首项

    // #错误 未对首项是否为NULL进行条件检测，导致段错误
    if(sll_oldfirst){
        PUTPTR(PREV_SLLP(sll_oldfirst), bp);
        // #错误，直接将指针保存在下一项的bp而不是前向指针处
        // 如不为NULL 将之前的首项块前向设置为当前块
    }

    if(TEST)
    printf("out set_sll\n");
}
static void delete_sll(void *bp){

    if(TEST)
    printf("into delete_sll bp=%p\n",bp);
    //函数或宏
    //将前一个节点的后向指针从当前节点更新为后一个节点
    //同时更新后一个节点的前向指针为前一个节点 如不为NULL
    void *next_sllp=NEXT_SLLP(bp);
    char *next_sllbp=GETPTR(next_sllp);
    void *prev_sllp=PREV_SLLP(bp);
    char *prev_sllbp=GETPTR(prev_sllp);

    if(TEST)
    printf("    delete_sll next_sllbp=%p prev_sllbp=%p\n"
        ,next_sllbp,prev_sllbp);
        //###错误delete_sll next_sllbp=0xeacc0020 prev_sllbp=0xeacc0020
        //当前块的前后指针都指向本身

    if(next_sllbp){
        // 如果下一个节点不为NULL
        PUTPTR(PREV_SLLP(next_sllbp), prev_sllbp);
        // 下一个节点的前向指针更新为当前节点的前向bp指针
    }

    PUTPTR(NEXT_SLLP(prev_sllbp), next_sllbp);

    // 上一个节点的后向指针更新为当前节点的后向指针
    // ##
    if(TEST)
    printf("out delete_sll\n");
}
// 合并空闲块
static void *coalesce(void *bp){
    if(TEST)
    printf("into coalesce\n");

    size_t prev_alloc = GET_PREV_ALLOC(HDRP(bp));
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    // 得到前后块的分配状态
    
    size_t size = GET_SIZE(HDRP(bp));

    if(TEST)
    printf("prev_alloc=%u next_alloc=%u size=%u\n",prev_alloc, next_alloc, size);

    if (prev_alloc && next_alloc) {           
        // 如不合并则无变化
        
    }else{
        // 如果合并则将空闲链表更新，然后更新块头脚
        delete_sll(bp);
        //从链表中删除当前块

        if (prev_alloc && !next_alloc) { 
            delete_sll(NEXT_BLKP(bp));

            size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
            PUT(HDRP(bp), PACK(size, prev_alloc, 0));
            PUT(FTRP(bp), PACK(size, prev_alloc, 0));
            // #错误 PUT(NEXT_BLKP(FTRP(bp)) 更新头部后使用FTRP即可到脚

        }else if (!prev_alloc && next_alloc) {   
            delete_sll(PREV_BLKP(bp));
            size_t prev_sllp_prev_alloc = GET_PREV_ALLOC(HDRP(PREV_BLKP(bp)));

            size += GET_SIZE(HDRP(PREV_BLKP(bp)));
            PUT(FTRP(bp), PACK(size, prev_sllp_prev_alloc, 0));
            PUT(HDRP(PREV_BLKP(bp)), PACK(size, prev_sllp_prev_alloc, 0));
            bp = PREV_BLKP(bp);

        }else {       
            delete_sll(NEXT_BLKP(bp));    
            delete_sll(PREV_BLKP(bp));
            size_t prev_sllp_prev_alloc = GET_PREV_ALLOC(HDRP(PREV_BLKP(bp)));
                           
            size += GET_SIZE(HDRP(PREV_BLKP(bp))) + 
            GET_SIZE(FTRP(NEXT_BLKP(bp)));
            PUT(HDRP(PREV_BLKP(bp)), PACK(size, prev_sllp_prev_alloc, 0));
            PUT(FTRP(NEXT_BLKP(bp)), PACK(size, prev_sllp_prev_alloc, 0));
            bp = PREV_BLKP(bp);
        }

        set_sll(bp, size);
        //添加合并后的空闲块到链表
    }
    
    CLEAN_ALLOC_TO_NEXT(bp);
    
    if(TEST)
    printf("out coalesce size=%u\n",size);

    return bp;
}

// 放置内容到空闲块
static void place(void *bp, size_t asize){
    
    if(TEST)
    printf("into place bp=%p, asize=%u\n",bp, asize);
    
    delete_sll(bp);
    //在信息被覆盖前从链表中删除当前空闲块

    size_t csize = GET_SIZE(HDRP(bp));
    size_t diff = csize-asize;
    // 放置容量与空闲块的差值为剩余块大小
    void *tp;
    size_t prev_alloc = GET_PREV_ALLOC(HDRP(bp));
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));

    if(TEST)
    printf("place csize=%u\n",csize);

    // #### 可优化 新增对后块的分配判断 
    // 如后块未分配，即使剩余块大小不足，仍可与后块合并

    if(!next_alloc){

        delete_sll(NEXT_BLKP(bp));
        diff += GET_SIZE(HDRP(NEXT_BLKP(bp)));
        //实现后似乎无区别，之前内存点数已达到49
        //删除后块，累加大小

        PUT(HDRP(bp), PACK(asize, prev_alloc, 1));
        PUT(FTRP(bp), PACK(asize, prev_alloc, 1));
        //设置当前块头部

        //此时tp为剩余块的bp位置
        tp = NEXT_BLKP(bp);
        PUT(HDRP(tp), PACK(diff, 0x2, 0));
        PUT(FTRP(tp), PACK(diff, 0x2, 0));
        set_sll(tp, diff);


    }else 
    if(diff >= MINBLOCKSIZE){
        // 如果剩余块大于等于最小块，则分割
        PUT(HDRP(bp), PACK(asize, prev_alloc, 1));
        PUT(FTRP(bp), PACK(asize, prev_alloc, 1));

        tp = NEXT_BLKP(bp);
        PUT(HDRP(tp), PACK(diff, 0x2, 0));
        PUT(FTRP(tp), PACK(diff, 0x2, 0));
        set_sll(tp, diff);
        //添加分割出的空闲块到链表

    }else{
        // 如不分割
        PUT(HDRP(bp), PACK(csize, prev_alloc, 1));
        PUT(FTRP(bp), PACK(csize, prev_alloc, 1));

        SET_ALLOC_TO_NEXT(bp);
        // 将当前块的分配状态更新到后一块
    }
    
    if(TEST)
    printf("out place\n");
}


static void place_realloc(void *bp, size_t asize, size_t csize){
    // printf("----into place_realloc-----\n");

    size_t diff = csize-asize;
    // 合并容量与放置容量的差值为剩余块大小
    void *tp;
    size_t prev_alloc = GET_PREV_ALLOC(HDRP(bp));

    if(diff >= MINBLOCKSIZE){
        // printf("--if(diff >= MINBLOCKSIZE)--\n");
        // 如果剩余块大于等于最小块，则分割
        PUT(HDRP(bp), PACK(asize, prev_alloc, 1));
        PUT(FTRP(bp), PACK(asize, prev_alloc, 1));
        // printblock(2,bp); 

        tp = NEXT_BLKP(bp);
        PUT(HDRP(tp), PACK(diff, 0x2, 0));
        PUT(FTRP(tp), PACK(diff, 0x2, 0));
        set_sll(tp, diff);
        //添加分割出的空闲块到链表
        // printblock(3,tp); 
        // printf("--end if(diff >= MINBLOCKSIZE)--\n");
    }else{
        // 如不分割
        PUT(HDRP(bp), PACK(csize, prev_alloc, 1));
        PUT(FTRP(bp), PACK(csize, prev_alloc, 1));
        // printblock(2,bp); 
        // printblock(3,NEXT_BLKP(bp)); 

        SET_ALLOC_TO_NEXT(bp);
        // 将当前块的分配状态更新到后一块
    }
    // printf("----out place_realloc-----\n");
}

static int printblock(int i, void *bp){
    size_t hsize, h_prev_alloc, halloc;
    char *headp;
    headp = (HDRP(bp));
    hsize = GET_SIZE(headp);
    h_prev_alloc = GET_PREV_ALLOC(headp);
    halloc = GET_ALLOC(headp);

    int res=0;
    if(hsize == 0){
        printf("##>>printblock EOF\n");
        res= 1;
    }

    printf("##>>printblock [%d]%p: header: [%u:%u:%u]\n",
        i, bp, hsize, h_prev_alloc, halloc);
    
    if(!halloc){
        printf("##>>printblock nextsslbp=%p, prevsslbp=%p\n",
            GETPTR(NEXT_SLLP(bp)),GETPTR(PREV_SLLP(bp)));
    }
    return res;
}

static void checkblock(void *bp){
    if((size_t)bp % 8){
        printf("##>>checkblock Error: %p is not 8 aligned\n",bp);
    }

}

static void checkheap(){
    printf("&&>>into checkheap\n");
    char *bp;
    int i;
    for(i=0, bp=heap_listp; printblock(i,bp)==0; i++,bp=NEXT_BLKP(bp)){
        checkblock(bp);
    }

    for(i=0, bp=heap_begin; i<SLLTYPE; i++,bp+=WSIZE){
        printf("&&>>ssl[%d] %p\n",i,GETPTR(bp));
    }
}


