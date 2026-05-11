/*
    下一次适配搜索
    见mm.c的#ifdef NEXT_FIT 
    定义全局变量指针rover 初始化为起始地址
    每次调用find的时候使用rover而不是局部变量搜索，
    从rover的旧位置到尾，再从头到rover的旧位置

    在合并空闲块的时候要检查rover的位置是否被合并，
    被合并时需将当前块的位置赋到rover
*/
