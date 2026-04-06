/* matrix multiply permutations */
#include <stdio.h>
#include <stdlib.h>
#include "mm.h"
#include "fcycmm.h"
#include "clock.h"
#include "csapp.h"

/* whether or not fcyc should clear the cache */
#define CLEARCACHE 1  

//线程数量
#define NTHREADS 6

/* global arrays */
array ga, gb, gc;

/* 编译选项

    gcc -O4 -Wall -mavx2 -o 12-34 12-34.c csapp.c clock.c fcycmm.c

*/

/* check the result array for correctness */
void checkresult(array c, int n)
{
    int i, j;

    for (i = 0; i < n; i++)
	for (j = 0; j < n; j++)
	    if (c[i][j] != (double)n) {
	      printf("Error: bad number (%f) in result matrix (%d,%d)\n", 
		       c[i][j], i, j);
	      fflush(stdout);
		exit(0);
	    }
}

/* Run f and return clocks per inner loop iteration */
double run(test_funct f, int n)
{
    double cpi;

    cpi = fcyc(f, n, CLEARCACHE) / (n*n*n);
    checkresult(gc, n);
    return(cpi);
}

/* reset result array to zero */
void reset(array c, int n)
{
    int i,j;
    
    for (i = 0; i < n; i++) {
	for (j = 0; j < n; j++) {
	    c[i][j] = 0.0;
	}
    }
}

/* initialize input arrays to 1 */
void init(array a, array b, int n) 
{
    int i,j;
    
    for (i = 0; i < n; i++) {
	for (j = 0; j < n; j++) {
	    a[i][j] = 1.0;
	    b[i][j] = 1.0;
	}
    }
}


/* print an array (debug) */
void printarray(array a, int n)
{
    int i, j;

    for (i = 0; i < n; i++) {
	for (j = 0; j < n; j++) {
	    printf("%5.1f ", a[i][j]);
	}
	printf("\n");
    }
}

/***********************************************
 * Six different versions of matrix multiply 
 ***********************************************/
void ijk(array A, array B, array C, int n) 
{
    int i, j, k;
    double sum;

/* $begin mm-ijk */
for (i = 0; i < n; i++) 
    for (j = 0; j < n; j++) {
	sum = 0.0;
        for (k = 0; k < n; k++)
            sum += A[i][k]*B[k][j];
        C[i][j] += sum;
    }
/* $end mm-ijk */

}

void jik(array A, array B, array C, int n) 
{
    int i, j, k;
    double sum;

/* $begin mm-jik */
for (j = 0; j < n; j++) 
    for (i = 0; i < n; i++) {
	sum = 0.0;
	for (k = 0; k < n; k++)
	    sum += A[i][k]*B[k][j];
	C[i][j] += sum;
    }
/* $end mm-jik */
}

void ikj_origin(array A, array B, array C, int n) 
{
    int i, j, k;
    double r;
    
    /* $begin mm-ikj */
for (i = 0; i < n; i++)
    for (k = 0; k < n; k++) {
	r = A[i][k];
	for (j = 0; j < n; j++)
	    C[i][j] += r*B[k][j];
    }
/* $end mm-ikj */
}

int check = 0;
//线程传递结构, 简单的使用全局结构
//或者在主线程内定义结构与线程id的另一个复合结构
struct thread_arg{
    double (*A)[MAXN+513];
    double (*B)[MAXN+513];
    double (*resC)[MAXN+513];
    // array C[NTHREADS];
    int n;
    long nelems_per_thread;
}pass_arg;
//线程版本 A/B矩阵读 C矩阵写
//!!不使用同步锁，转而创建与线程数量对应的缓存矩阵
//!!之后在主线程中累加
// ####然而工作线程按行分配，彼此不存在冲突，可直接累计到C
// ####并且之前初始化buf的memset花费了大量时间
void *thread_ikj(void *vargp){
    int i, j, k;
    double r;
    long myid = *((long *)vargp); 
    long start = myid * pass_arg.nelems_per_thread; 
    long end = start + pass_arg.nelems_per_thread; 
    if(end > pass_arg.n){
        end = pass_arg.n;
    }
    // if(check){
    //     printf("[%ld] start=%ld, end=%ld\n",myid, start, end);
    // }
    
    for (i = start; i < end; i++){
        for (k = 0; k < pass_arg.n; k++) {
            r = pass_arg.A[i][k];
            for (j = 0; j < pass_arg.n; j++){
                pass_arg.resC[i][j] += r*pass_arg.B[k][j];
            }
        }
    }

    return NULL;
}
//累计线程缓冲计算结果到C
// void thread_add(array C, long myid, int n){
//     long start = myid * pass_arg.nelems_per_thread; 
//     long end = start + pass_arg.nelems_per_thread; 
//     if(end > pass_arg.n){
//         end = pass_arg.n;
//     }
//     for(int i = start; i<end ;i++){
//         for(int j = 0; j<n; j++){
//             C[i][j]+=pass_arg.C[myid][i][j];
//         }
//     }
// }
// void *thread_ikj_sum(void *vargp){
//     long myid = *((long *)vargp); 
//     long start = myid * pass_arg.nelems_per_thread; 
//     long end = start + pass_arg.nelems_per_thread; 
//     if(end > pass_arg.n){
//         end = pass_arg.n;
//     }
//     for(int i = start; i<end ;i++){
//         for(int j = 0; j<pass_arg.n; j++){
//             pass_arg.resC[i][j]+=pass_arg.C[myid][i][j];
//         }
//     }   
// }
void ikj(array A, array B, array C, int n) 
{
    long i, myid[NTHREADS];
    pthread_t tid[NTHREADS];  
    // printf("n=%d,nelems_per_thread=%d\n",n,nelems_per_thread);
    
    pass_arg.n = n;
    pass_arg.A = A;
    pass_arg.B = B;
    pass_arg.resC = C;
    pass_arg.nelems_per_thread = 
        (n + (NTHREADS - 1)) / NTHREADS;
    if(check){
        printf("nelems_per_thread=%ld\n",pass_arg.nelems_per_thread);
    }
    //创建线程、初始化全局变量、传递线程id参数
    for (i = 0; i < NTHREADS; i++) {   
        // memset(pass_arg.C[i], 0, sizeof(pass_arg.C[i]));             
	    myid[i] = i;                                  
	    Pthread_create(&tid[i], NULL, thread_ikj, &myid[i]); 
    }             
    //回收线程 并累计
    for (i = 0; i < NTHREADS; i++){                  
	    Pthread_join(tid[i], NULL); 
        // thread_add(C, myid[i], n);
    }
    // !! 如继续优化，则将thread_add转为线程版本
    // for (i = 0; i < NTHREADS; i++) {   
	//     Pthread_create(&tid[i], NULL, thread_ikj_sum, &myid[i]); 
    // }   

    // for (i = 0; i < NTHREADS; i++){                  
	//     Pthread_join(tid[i], NULL); 
    //     // thread_add(C, myid[i], n);
    // }
}


void kij(array A, array B, array C, int n)
{
    int i, j, k;
    double r;

    /* $begin mm-kij */
for (k = 0; k < n; k++)
    for (i = 0; i < n; i++) {
	r = A[i][k];
	for (j = 0; j < n; j++)
	    C[i][j] += r*B[k][j];
    }
/* $end mm-kij */
}

void kji(array A, array B, array C, int n)
{
    int i, j, k;
    double r;

/* $begin mm-kji */
for (k = 0; k < n; k++)
    for (j = 0; j < n; j++) {
	r = B[k][j];
	for (i = 0; i < n; i++)
	    C[i][j] += A[i][k]*r;
    }
/* $end mm-kji */
}

void jki(array A, array B, array C, int n)
{
    int i, j, k;
    double r;

/* $begin mm-jki */
for (j = 0; j < n; j++)
    for (k = 0; k < n; k++) {
	r = B[k][j];
	for (i = 0; i < n; i++)
	    C[i][j] += A[i][k]*r;
    }
/* $end mm-jki */
}

/* 
 * Run the six versions of matrix multiply and display performance
 * as clock cycles per inner loop iteration.
 */ 

int main()
{
    int n;

    init(ga, gb, MAXN);

    printf("matmult cycles/loop iteration\n");
    printf("%3s%6s%6s%6s%6s%6s%6s\n", "n", 
	   "jki", "kji", "ijk", "jik", "kij", "ikj");
    fflush(stdout);
    for (n = MINN; n <= MAXN; n += INCN) {  
	printf("%3d ", n);

	// printf("%5.2f ", run(jki, n));
	// printf("%5.2f ", run(kji, n));
	// printf("%5.2f ", run(ijk, n));
	// printf("%5.2f ", run(jik, n));
	printf("%5.2f ", run(kij, n));
	printf("%5.2f ", run(ikj, n));
	printf("\n");
	fflush(stdout);
    }
    exit(0);
}

