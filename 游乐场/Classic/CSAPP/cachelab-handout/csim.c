#include "cachelab.h"
#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
/*
    接收命令行参数 s E b
        动态内存分配空间
    使用valgrind文件进行内存模拟
        忽略I开头的指令行，数据行M/L/S开头有空格
    输出命中/未命中/驱逐总数
    使用最不常用替换策略驱逐缓存行 !! ###翻译错误 是最近最少使用 也就是时间最久
    ./csim-ref -v -s 2 -E 1 -b 4 -t traces/dave.trace
    ./csim -s 2 -E 1 -b 4 -t traces/dave.trace
    
    创造一个二维结构数组来表示信息
    flag/t/s 表示块，而不是与块一起创造为完整的缓存的位表示
    如果在S中有效位与标识位匹配则存在
    行表示S
    列表示E
    元素内容包括有效位/标识位，以及替换策略的使用次数  ### 换为录入顺序
*/
struct cache_struct{
    int DirtyBit;
    int cache_t_bits;
    int count;
};
struct cache_struct * _create_cache(int cache_block){
    struct cache_struct *cache;
    long size=cache_block*sizeof(struct cache_struct);
    cache=(struct cache_struct*)malloc(size);// # 之前只填入数量而没有*结构大小
    if(cache==NULL){
        perror("malloc error");
        exit(0);
    }
    memset(cache,0,size);
    return cache; 
}
unsigned _creat_mask(int n){
    unsigned res=0;
    for(int i=1;i<=n;i++){
        res=(res<<1)|1;// # 将|写为&，导致mask为0
    }
    return res;
}
int main(int argc, char *argv[])
{
/*    for(int i=1;i<argc;i++){
        printf("argv %d:%s\n",i,argv[i]);
    }
*/
    int opt,cache_s,cache_E,cache_b,show_test=0;
    char *file_t;
    const char *optstring = "vs:E:b:t:";// v报错，v没有参数不加':'
    while ((opt=getopt(argc,argv,optstring))!=-1){
        /* 如果 getopt（） 被重复调用，则
            依次返回每个 Option Characters 中的每个 Option 字符
            option 元素。*/
        //如果没有更多选项字符， 则 getopt（） 返回 -1
        switch(opt){
            case 's':
                cache_s=atoi(optarg);
                // printf("getopt %c:%d\n",opt,cache_s);
                break;
            case 'E':
                cache_E=atoi(optarg);
                // printf("getopt %c:%d\n",opt,cache_E);
                break;
            case 'b':
                cache_b=atoi(optarg);
                // printf("getopt %c:%d\n",opt,cache_b);
                break;
            case 't':
                file_t=optarg;
                // printf("getopt %c:%s\n",opt,file_t);
                break;
            case 'v':
                show_test=1;
                // printf("getopt %c:%s\n",opt,file_t);
                break;
        }
    }

//  int cache_DirtyBit=2;
    int cache_S=pow(2,cache_s);
//  int cache_B=pow(2,cache_b);
//  int cache_C=cache_S*cache_E*cache_B*cache_DirtyBit;
    int cache_block=cache_S*cache_E;
//  unsigned char *cache;
    struct cache_struct *cache;
    cache=_create_cache(cache_block);
    if(show_test){
        printf("cache_block %d\n",cache_block);
    }



    FILE *fp;
    char fdata[20];
    if((fp=fopen(file_t,"r"))==NULL){
        perror("File open error");
        exit(0);
    }
//  while(!feof(fp)){ 
    char ins;
    unsigned long addr,size,ishit;
    unsigned long data_TS,data_T,data_S,mask,search_S,emptycache,LRUindex,LRUcount,sequences=1;
    unsigned hits,misses,evictions,loopindex;
    hits=misses=evictions=0;
    mask=_creat_mask(cache_s);
    while(fgets(fdata,20,fp)!=NULL){
//      printf("%s",fdata);
//      sscanf(fdata," %c %ld,%ld",&ins,&addr,&size);
// # 地址为十六进制
        sscanf(fdata," %c %lx,%ld",&ins,&addr,&size);// ## addr为long 十六进制也要有l 为lx
        // windows系统long为4字节，linux为8字节，在windows 使用long读取8字节地址将溢出
        if(!(ins=='L'||ins=='S'||ins=='M')){//排除指令I
            continue;
        }
        if(show_test){
            printf("sscanf %c %lx %ld",ins,addr,size);
        }
        
// 使用无符号

        data_TS=addr>>cache_b;// ### 类型为unsigned long long 时右移出现有规律的随机数
        data_S=data_TS&mask;
        data_T=data_TS>>cache_s;
        search_S=data_S*cache_E;
        if(show_test){
            printf("%ld\n",search_S);
            printf("  addr=%lu,data_T=%ld,data_S=%ld ",addr,data_T,data_S);
        }
        
        ishit=0;
        // 定位S
        loopindex=search_S;
        for(int i=1;i<=cache_E;i++){
        // E次循环
            if(cache[loopindex].DirtyBit==1&&cache[loopindex].cache_t_bits==data_T){
                //检查有效位与标记位，如果存在则命中
                ishit=1;
                break;
            }
            loopindex++;
        }
        if(ishit){
            hits++;
            cache[loopindex].count=sequences++;
            if(show_test){
                printf("    hits");
            }
        }else{
            misses++;
            if(show_test){
                printf("    misses");
            }
            //如果miss则加载到缓存
            //遍历E寻找空缓存
            emptycache=0;
            loopindex=search_S;
            for(int i=1;i<=cache_E;i++){
                // printf(" DirtyBit=%d ",cache[loopindex].DirtyBit);
                if(cache[loopindex].DirtyBit==0){
                    emptycache=1;
                    break;
                }
                loopindex++;
            }
            if(!emptycache){
                //如果找不到空缓存则遍历查找最不常用的替换
                loopindex=search_S;
                LRUindex=loopindex;// ### 查找角标应当从S所在行开始
                LRUcount=cache[loopindex].count;
                for(int i=1;i<=cache_E;i++){
                    if(cache[loopindex].count<LRUcount){
                        LRUindex=loopindex;// #之前写为 =1 没有得到LRU元素的角标
                        LRUcount=cache[loopindex].count;
                    }
                    loopindex++;
                }        
                evictions++; 
                loopindex=LRUindex;// #之前没有在循环结束后更新后面要用的角标
                if(show_test){
                    printf("    eviction t=%d",cache[loopindex].cache_t_bits);  
                }
            }
            //在空或替换位置存入新数据
            if(show_test){
                printf("    loopindex=%d",loopindex); 
            }
            cache[loopindex].count=sequences++;
            cache[loopindex].cache_t_bits=data_T;
            cache[loopindex].DirtyBit=1; 
        }
        if(ins=='M'){// 如果为 M则有第二次
            hits++;
            cache[loopindex].count=sequences++;
            if(show_test){
                printf("    hits");
            }
        } 
        if(show_test){
            printf("\n");
        }
    }

    
    if(ferror(fp)){
		perror("file r/w error");
	}else if(feof(fp)&&show_test){
// feof用来判断是否成功读取到文件结尾
		printf("EOF success\n");
	}
    if(fclose(fp)){
        perror("File close error");
        exit(0);
    }
    printSummary(hits,misses,evictions);
    if(show_test){
        printf("hits=%d,misses=%d,evictions=%d",hits,misses,evictions);
    }
    return 0;
}
