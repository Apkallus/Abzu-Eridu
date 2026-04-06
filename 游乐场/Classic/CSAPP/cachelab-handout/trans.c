/* 
 * trans.c - Matrix transpose B = A^T
 *
 * Each transpose function must have a prototype of the form:
 * void trans(int M, int N, int A[N][M], int B[M][N]);
 *
 * A transpose function is evaluated by counting the number of misses
 * on a 1KB direct mapped cache with a block size of 32 bytes.
 * 
 * 通过计算块大小为 32 字节的 1KB 直接映射高速缓存的未命中次数来评估转置函数。
 * 1个块 32/4=8个int
 * 缓存 1024/32=32个块 1024/4=256个元素 1024/4/(8*8)=4个8*8块
 * 每个矩阵 32/2=16个块
 * 

 */ 
#include <stdio.h>
#include "cachelab.h"
#define block 8
#define bigblock 16
#define lee 4
int is_transpose(int M, int N, int A[N][M], int B[M][N]);

/* 
 * transpose_submit - This is the solution transpose function that you
 *     will be graded on for Part B of the assignment. Do not change
 *     the description string "Transpose submission", as the driver
 *     searches for that string to identify the transpose function to
 *     be graded. 
 * 
 * transpose_submit - 这是您将在作业 B 部分中被评分的解决方案转置函数。
 *      请勿更改描述字符串 “Transpose submission”，
 *      因为驱动程序会搜索该字符串来识别要评分的转置函数。
 * 
 *      函数内最多定义12个int局部变量
 *      无递归，无数组，无内存分配
 * 
 *      对角线的冲突不命中
 */
char transpose_submit_desc[] = "Transpose submission";
void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{
    /*
        61*67 hits:6216, misses:2023, evictions:1991
    */
    int i, j, n, m;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    n=N-N%8;
    m=M-M%8;
    
    for (j = 0; j < m; j+=8) {  
        for (i = 0; i < n; i++) {                 
            t0 = A[i][j];
            t1 = A[i][j+1];
            t2 = A[i][j+2];
            t3 = A[i][j+3];
            t4 = A[i][j+4];
            t5 = A[i][j+5];
            t6 = A[i][j+6];
            t7 = A[i][j+7];
            B[j][i] = t0;
            B[j+1][i] = t1;
            B[j+2][i] = t2;
            B[j+3][i] = t3;
            B[j+4][i] = t4;
            B[j+5][i] = t5;
            B[j+6][i] = t6;
            B[j+7][i] = t7;
        }
    }  
    for (j = 0; j < M; j++) {  
        for (i = n; i < N; i++) {   
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }
    for (j = m; j < M; j++) {  
        for (i = n; i < N; i++) {   
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }
    for (j = m; j < M; j++) {  
        for (i = 0; i < N; i++) {   
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }

}

/* 
 * You can define additional transpose functions below. We've defined
 * a simple one below to help you get started. 
 *  你可以在下面定义更多的转置函数。
 *  我们在下面定义了一个简单的函数，以帮助您开始使用。
 */ 

 // 对调临近对角线块
char trans_a[] = "transpose_a";
void transa(int M, int N, int A[N][M], int B[M][N])
{
/*
    32  hits:2289, misses:276, evictions:244
    64  hits:4545 misses:4676 evictions:4644 block=8
    64  hits:6353, misses:2356, evictions:2324 block=4
    
*/   
    int i, j, flag=0, ii, jj, ix, jx, jt;
    int t0;
    
    for (i = 0; i < N; i+=block){  
        for (j = 0; j < M; j+=block) { 
            if(i!=j){
                for (ii = i; ii < i+block; ii++) { 
                    for(jj = j; jj < j+block; jj++){
                        t0 = A[ii][jj];
                        B[jj][ii] = t0;
                    }        
                }
            }else{
                if(flag==0||flag==2){
                    flag = 1;   
                    // ix=i+block*N+block;
                    // jx=j+block*M+block;    
                    ix=i+block;
                    jx=j+block;       
                }else{
                    flag = 2;
                    // ix=i-block*N-block;  当前使用二维数组索引而不是一维数组索引
                    // jx=j-block*M-block;  
                    ix=i-block;  
                    jx=j-block;   
                }
                for (ii = i; ii < i+block; ii++, ix++) { 
                    // for(jj = j; jj < j+block; jj++, jx++){ 内循环jx没有初始化导致持续累积
                    for(jj = j, jt = jx; jj < j+block; jj++, jt++){
                        t0 = A[ii][jj];
                        // B[jx][ix] = t0;
                        B[jt][ix] = t0;
                    }        
                }
            }
            if(flag==2){
                flag = 0;
                // ix=i-block*N-block;  
                // jx=j-block*M-block;
                ix=i-block;  
                jx=j-block;
                for (ii = i; ii < i+block; ii++, ix++) { 
                    // for(jj = j; jj < j+block; jj++, jx++){
                    for(jj = j, jt = jx; jj < j+block; jj++, jt++){
                        // t0 = B[ii][jj];
                        // B[ii][jj] = B[jx][ix]; 在行列调换后应当直接对应而不是再次调换行列
                        // B[jx][ix] = t0;
                        t0 = B[ii][jj];
                        B[ii][jj] = B[ix][jt];
                        B[ix][jt] = t0;                    
                    }        
                }               
            }


        }  
    }
}
char trans_a2[] = "transpose_a2";
void transa2(int M, int N, int A[N][M], int B[M][N])
{
/*
    32  hits:2289, misses:276, evictions:244
    64  hits:4545 misses:4676 evictions:4644 
    64  hits:6737, misses:1972, evictions:1940 block=4,lee=4

    即使数组a循环展开4，数据没有变化
    应当从访问模式入手
*/   
    int i, j, flag=0, ii, jj, ix, jx, jt;
    int t0, t1, t2, t3;
    
    for (i = 0; i < N; i+=block){  
        for (j = 0; j < M; j+=block) { 
            if(i!=j){
                for (ii = i; ii < i+block; ii++) { 
                    for(jj = j; jj < j+block-lee+1; jj+=lee){
                        t0 = A[ii][jj];
                        t1 = A[ii][jj+1];
                        t2 = A[ii][jj+2];
                        t3 = A[ii][jj+3];
                        B[jj][ii] = t0;
                        B[jj+1][ii] = t1;
                        B[jj+2][ii] = t2;
                        B[jj+3][ii] = t3;
                    }        
                }
            }else{
                if(flag==0||flag==2){
                    flag = 1;   
                    // ix=i+block*N+block;
                    // jx=j+block*M+block;    
                    ix=i+block;
                    jx=j+block;       
                }else{
                    flag = 2;
                    // ix=i-block*N-block;  当前使用二维数组索引而不是一维数组索引
                    // jx=j-block*M-block;  
                    ix=i-block;  
                    jx=j-block;   
                }
                for (ii = i; ii < i+block; ii++, ix++) { 
                    // for(jj = j; jj < j+block; jj++, jx++){ 内循环jx没有初始化导致持续累积
                    for(jj = j, jt = jx; jj < j+block-lee+1; jj+=lee, jt+=lee){
                        t0 = A[ii][jj];
                        t1 = A[ii][jj+1];
                        t2 = A[ii][jj+2];
                        t3 = A[ii][jj+3];
                        // B[jx][ix] = t0;
                        B[jt][ix] = t0;
                        B[jt+1][ix] = t1;
                        B[jt+2][ix] = t2;
                        B[jt+3][ix] = t3;
                    }        
                }
            }
            if(flag==2){
                flag = 0;
                // ix=i-block*N-block;  
                // jx=j-block*M-block;
                ix=i-block;  
                jx=j-block;
                for (ii = i; ii < i+block; ii++, ix++) { 
                    // for(jj = j; jj < j+block; jj++, jx++){
                    for(jj = j, jt = jx; jj < j+block-lee+1; jj+=lee, jt+=lee){
                        // t0 = B[ii][jj];
                        // B[ii][jj] = B[jx][ix]; 在行列调换后应当直接对应而不是再次调换行列
                        // B[jx][ix] = t0;
                        t0 = B[ii][jj];
                        t1 = B[ii][jj+1];
                        t2 = B[ii][jj+2];
                        t3 = B[ii][jj+3];
                        B[ii][jj] = B[ix][jt];
                        B[ii][jj+1] = B[ix][jt+1];
                        B[ii][jj+2] = B[ix][jt+2];
                        B[ii][jj+3] = B[ix][jt+3];
                        B[ix][jt] = t0;     
                        B[ix][jt+1] = t1;  
                        B[ix][jt+2] = t2;  
                        B[ix][jt+3] = t3;                 
                    }        
                }               
            }


        }  
    }
}

// 即将使用的块作为中转
char trans_b[] = "transpose_b";
void transb(int M, int N, int A[N][M], int B[M][N])
{
/*
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 *      1 2 3 4 1
 * 
    32  hits:2548, misses:529, evictions:497 不命中超出预期
    32  hits:2809, misses:268, evictions:236 处理第一块的严重冲突后
    64  x
*/ 
    int i, j, flag=0, ii, jj, ix, jx, jt, it, ia, ja;
    int t0;
    for (i = 0; i < N; i+=block){  
        for (j = 0; j < M; j+=block) { 
            flag++;//计算block顺序
//          else{// # !! flag信号不匹配
            // if(flag==1||flag==3||flag==5||flag==7){
            if(flag==1||flag==3||flag==4||flag==5){
                // if(flag==1){// a1-b11 b11-b1 !!!!!! 3次移动都使用同一内存大块，全冲突
                //     // jx与lx b到下一行 b1-b11
                //     ix=i;
                //     jx=j+block;
                    
                //     // a1
                //     ia=i;
                //     ja=j;
                if(flag==1){// a1-b2 b2-b1 
                    //b1-b2
                    ix=i+block;
                    jx=j;
                    //a1
                    ia=i;
                    ja=j;
                }else if(flag==3){// a22-b111 b111-b22
                    // jx与lx b到下一行 b11-b111 !! #当于间接交换中间接一般交换时
                    // 此时a/b已经移动到了下一个块 b111 
                    ix=i;
                    jx=j;

                    // a2-a22 !! a3-a22
                    ia=i+block;
                    ja=j-block;
                }else if(flag==4){// a333-b1111 b1111-b333
                    // jx与lx b到下一行 b111-b1111 !!
                    // 此时a/b已经移动到了下一个块 b1111
                    ix=i;
                    jx=j;

                    // a4-a333
                    ia=i+2*block;
                    ja=j-block;
                }else if(flag==5){              //  a4444-b2 b2-b4444 
                    // jx与lx b行-3 列+1 b1111-b2 !!
                    // 此时a/b已经移动到了下一个块 b2
                    ix=i;
                    jx=j;   

                    // a4-a4444 !!
                    // a11-a4444
                    ia=i+2*block;
                    ja=j+3*block;   
                }
                // else{
                //     continue;//对角线则跳过
                // }

                // a间接转移到下一个要用的b块
                // for (ii = ia, it = ix; ii < i+block; ii++, it++){ 
                //     for(jj = ja, jt = jx; jj < j+block; jj++, jt++){ 更换变量后没有更换循环条件
                for (ii = ia, it = ix; ii < ia+block; ii++, it++){ 
                    for(jj = ja, jt = jx; jj < ja+block; jj++, jt++){
                        t0 = A[ii][jj];
                        B[jt][it] = t0;
                    }        
                }
                // 从中转b块到对应b块
                for (ii = ia, it = ix; ii < ia+block; ii++, it++){ 
                    for(jj = ja, jt = jx; jj < ja+block; jj++, jt++){ 
                        t0 = B[jt][it];
                        B[jt][it] = B[jj][ii];  // # 未更换上一个函数的角标 导致中转为空
                        B[jj][ii] = t0;                    
                    }        
                }
                //  每次间接转移后接普通转移，确保间接转移使用的块能够在后面立即复用
                //  重复直到对角线4个块都转移
            }

            // #将普通调换移动到间接转移后
            if(!(flag==1||flag==6||flag==11||flag==16)){
                // 当间接转移后接普通调换时，不应使用排除的if else语句
                // 只排除对角线
                //x1 o2 x3 o4 x5 o6 x7 o~
                // 1 6 11 16
                for (ii = i; ii < i+block; ii++) { 
                    for(jj = j; jj < j+block; jj++){
                        t0 = A[ii][jj];
                        B[jj][ii] = t0;
                    }        
                }
            }
            flag%=16;// 缓存 1024/4/(8*8)=4个8*8块
        }  
    }
}
// 即将使用的块作为中转，精简并调整后能够处理64
// 将a1-b2-b1
// a22-b11-b22
// a33-b22-b33
char trans_b2[] = "transpose_b2";
void transb2(int M, int N, int A[N][M], int B[M][N])
{
/*
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 * 256  1 2 3 4 1
 *      1 2 3 4 1
 *     
 *  

    32  hits:2548, misses:529, evictions:497
    32  hits:2809, misses:268, evictions:236 处理第一块的严重冲突后
    64  hits:5633, misses:6660, evictions:6628
    64  hits:10277, misses:2016, evictions:1984 bigblock=16,block=4

*/ 
    int i, j, flag=0, ii, jj, ix, it, jo, io;
    int t0;
    for (io = 0; io < N; io+=bigblock){  
        for (jo = 0; jo < M; jo+=bigblock) { 
            for (i = io; i < io+bigblock; i+=block){  
                for (j = jo; j < jo+bigblock; j+=block) { 
                    flag++;//计算block顺序
        //          else{// # !! flag信号不匹配
                    // if(flag==1||flag==3||flag==5||flag==7){
                    if(flag==1||flag==2||flag==3||flag==4){
                        if(flag==1){// a1-b2 b2-b1 
                            //b1-b2
                            ix=i+block;
                            //a1
                        }else{//  合并
                            // b1111
                            ix=i;
                            // a4-a4444
                        }

                        // a间接转移到下一个要用的b块
                        // i+(flag-1)*block 为对应偏移
                        for (ii = i+(flag-1)*block, it = ix; ii < i+(flag-1)*block+block; ii++, it++){ 
                            for(jj = j; jj < j+block; jj++){
                                t0 = A[ii][jj];
                                B[jj][it] = t0;
                            }        
                        }                
                        // printf("flag = %d s\n",flag);
                        // printmt(N,M,B);
                        
                        // 从中转b块到对应b块
                        for (ii = i+(flag-1)*block, it = ix; ii < i+(flag-1)*block+block; ii++, it++){ 
                            for(jj = j; jj < j+block; jj++){ 
                                t0 = B[jj][it];
                                B[jj][it] = B[jj][ii];  // # 未更换上一个函数的角标 导致中转为空
                                B[jj][ii] = t0;                    
                            }        
                        }
                        
                        // printf("flag = %d x\n",flag);
                        // printmt(N,M,B);
                        //  每次间接转移后接普通转移，确保间接转移使用的块能够在后面立即复用
                        //  重复直到对角线4个块都转移
                    }

                    // #将普通调换移动到间接转移后
                    if(!(flag==1||flag==6||flag==11||flag==16)){
                        // 只排除对角线
                        //x1 o2 x3 o4 x5 o6 x7 o~
                        // 1 6 11 16
                        for (ii = i; ii < i+block; ii++) { 
                            for(jj = j; jj < j+block; jj++){
                                t0 = A[ii][jj];
                                B[jj][ii] = t0;
                            }        
                        }
                        
                        // printf("flag = %d\n",flag);
                        // printmt(N,M,B);
                    }
                    flag%=16;// 缓存 1024/4/(8*8)=4个8*8块
                }  
      
            }     
        }       
    }
}
/* 
 * trans - A simple baseline transpose function, not optimized for the cache.
 */
char trans_desc[] = "Simple row-wise scan transpose";
void trans(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    
    for (j = 0; j < M; j+=8) {  
        for (i = 0; i < N; i++) {                 
            t0 = A[i][j];
            t1 = A[i][j+1];
            t2 = A[i][j+2];
            t3 = A[i][j+3];
            t4 = A[i][j+4];
            t5 = A[i][j+5];
            t6 = A[i][j+6];
            t7 = A[i][j+7];
            B[j+0][i] = t0;
            B[j+1][i] = t1;
            B[j+2][i] = t2;
            B[j+3][i] = t3;
            B[j+4][i] = t4;
            B[j+5][i] = t5;
            B[j+6][i] = t6;
            B[j+7][i] = t7;
        }
    }  
}

char trans_c[] = "Transpose c";
void transc(int M, int N, int A[N][M], int B[M][N])
{
/*
    32  hits:3457, misses:388, evictions:356
    64  hits:12033, misses:3332, evictions:3300 lee=8
    64  hits:12225, misses:2116, evictions:2084 lee=4
    复制后在B内转置
*/   
    int i, j, k=0, g=0;
    int t0, t1, t2, t3, t6, t7;
    // int t4, t5, ;
    
    //复制
    for (i = 0; i < N; i++){  
        if(i&&i%(M/(N/lee))==0){// 内循环为M/lee次 M/N/lee=lee次填满一轮
            g=0;    // 移动到下一段时重置为0
            k+=lee; // 行偏移lee 
        }
        for (j = 0; j <= M-lee; j+=lee) { 
            t0=A[i][j];
            t1=A[i][j+1];
            t2=A[i][j+2];
            t3=A[i][j+3];
            // t4=A[i][j+4];
            // t5=A[i][j+5];
            // t6=A[i][j+6];
            // t7=A[i][j+7];
            
            B[j+g][k]=t0;
            B[j+g][k+1]=t1;
            B[j+g][k+2]=t2;
            B[j+g][k+3]=t3;
            // B[j+g][k+4]=t4;
            // B[j+g][k+5]=t5;
            // B[j+g][k+6]=t6;
            // B[j+g][k+7]=t7;    
        }
        g++;    // 从下一行开始  
            
    }
    // printmt(N,M,B); 
    for (k = 0; k < N; k+=lee) {
        for (g = 0; g < M; g+=lee) { 
            for (i = k; i < k+lee; i++) {
                for (j = g; j < g+lee; j++) { 
                    // if(i>j){ 
                    if(i-k>j-g){// ## 分块内计算角标时应当计算基准后再比较或对调
                        t6=i-k+g;
                        t7=j-g+k;
                        t0 = B[i][j];
                        B[i][j] =B[t7][t6];
                        B[t7][t6] = t0;
                        
                    }
                }
            }
        }
    }
    // printmt(N,M,B);
}

char trans_d[] = "Transpose d@";
void transd(int M, int N, int A[N][M], int B[M][N])
{
    /*
        1 2
        3 4
        64 hits:9081, misses:1164, evictions:1132
    */
    int i, j, ii, jj;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    
    for (i = 0; i < N; i+=8) {
        for (j = 0; j < M; j+=8) {  //block 8

            for (ii = i; ii < i+4; ii++) {// a1-b1 a2-b2                 
                // a1
                t0 = A[ii][j];
                t1 = A[ii][j+1];
                t2 = A[ii][j+2];
                t3 = A[ii][j+3];

                // a2
                t4 = A[ii][j+4];
                t5 = A[ii][j+5];
                t6 = A[ii][j+6];
                t7 = A[ii][j+7];

                // a1-b1
                B[j][ii] = t0;
                B[j+1][ii] = t1;
                B[j+2][ii] = t2;
                B[j+3][ii] = t3;

                // a2-b2
                B[j][ii+4] = t4;
                B[j+1][ii+4] = t5;
                B[j+2][ii+4] = t6;
                B[j+3][ii+4] = t7;
            }
            // ii=block/2 8/2=4
            for(jj = j; jj < j+4; jj++){
                // a3 读一列 由于之前的b2按照转置后的行保存
                // 之后把a3列放入b2行
                t0 = A[ii][jj];
                t1 = A[ii+1][jj];
                t2 = A[ii+2][jj];
                t3 = A[ii+3][jj];

                // b2读一行
                t4 = B[jj][ii];
                t5 = B[jj][ii+1];
                t6 = B[jj][ii+2];
                t7 = B[jj][ii+3];

                // b2得到a3
                B[jj][ii] = t0;
                B[jj][ii+1] = t1;
                B[jj][ii+2] = t2;
                B[jj][ii+3] = t3;

                // b3得到b2
                B[jj+4][i] = t4; 
                B[jj+4][i+1] = t5;
                B[jj+4][i+2] = t6;
                B[jj+4][i+3] = t7;
            }
            // jj=4
            for (ii = i+4; ii < i+8; ii+=2) {// a4-b4    不知为何超时后又通过
            // for (ii = i+4; ii < i+8; ii++) {// a4-b4             
                // a4.1
                t0 = A[ii][jj];
                t1 = A[ii][jj+1];
                t2 = A[ii][jj+2];
                t3 = A[ii][jj+3];

                // a4.2                 
                t4 = A[ii+1][jj];
                t5 = A[ii+1][jj+1];
                t6 = A[ii+1][jj+2];
                t7 = A[ii+1][jj+3];

                // a4.1-b4.1
                B[jj][ii] = t0;
                B[jj+1][ii] = t1;
                B[jj+2][ii] = t2;
                B[jj+3][ii] = t3;

                // a4.2-b4.2
                B[jj][ii+1] = t4;
                B[jj+1][ii+1] = t5;
                B[jj+2][ii+1] = t6;
                B[jj+3][ii+1] = t7;
            }
        }
    }  
}
void transe(int M, int N, int A[N][M], int B[M][N])
{
    /*
        61*67 hits:6216, misses:2023, evictions:1991
    */
    int i, j, n, m;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    n=N-N%8;
    m=M-M%8;
    
    for (j = 0; j < m; j+=8) {  
        for (i = 0; i < n; i++) {                 
            t0 = A[i][j];
            t1 = A[i][j+1];
            t2 = A[i][j+2];
            t3 = A[i][j+3];
            t4 = A[i][j+4];
            t5 = A[i][j+5];
            t6 = A[i][j+6];
            t7 = A[i][j+7];
            B[j][i] = t0;
            B[j+1][i] = t1;
            B[j+2][i] = t2;
            B[j+3][i] = t3;
            B[j+4][i] = t4;
            B[j+5][i] = t5;
            B[j+6][i] = t6;
            B[j+7][i] = t7;
        }
    }  
    for (i = n; i < N; i++) { 
        for (j = m; j < M; j++) {           
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }
    for (i = 0; i < N; i++) {
        for (j = m; j < M; j++) {       
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }      
    for (i = n; i < N; i++) {  
        for (j = 0; j < M; j++) { 
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }
}
/*
 * registerFunctions - This function registers your transpose
 *     functions with the driver.  At runtime, the driver will
 *     evaluate each of the registered functions and summarize their
 *     performance. This is a handy way to experiment with different
 *     transpose strategies.
 *  registerFunctions - 该函数用于向驱动程序注册转置函数。 
 *      运行时，驱动程序将评估每个注册函数并总结其性能。
 *      这是一种实验不同转置策略的便捷方法。
 */
void registerFunctions()
{
    /* Register your solution function 
    *   注册解决方案函数
    */
    registerTransFunction(transpose_submit, transpose_submit_desc); 

    /* Register any additional transpose functions 
    * 注册其他转置函数 
    */
    registerTransFunction(transc, trans_c); 
    // registerTransFunction(transb, trans_b); 
}

/* 
 * is_transpose - This helper function checks if B is the transpose of
 *     A. You can check the correctness of your transpose by calling
 *     it before returning from the transpose function.
 * is_transpose - 这个辅助函数用于检查 B 是否是 A 的转置。
 */
int is_transpose(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; ++j) {
            if (A[i][j] != B[j][i]) {
                return 0;
            }
        }
    }
    return 1;
}

