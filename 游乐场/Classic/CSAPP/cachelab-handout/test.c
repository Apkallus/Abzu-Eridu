#include <stdio.h>
#include <string.h>
#include "cachelab.h"
#define block 8
#define bigblock 32
#define lee 4
void printmt(int row, int col, int array[row][col]);
int is_transpose(int M, int N, int A[N][M], int B[M][N]);
/*
    gcc test.c -o test_l; ./test_l > rec.txt
*/ 

void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{
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
    for (j = m; j < M; j++) {  
        for (i = 0; i < N; i++) {   
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
    for (j = 0; j < M; j++) {  
        for (i = n; i < N; i++) {   
            t0 = A[i][j];
            B[j][i] = t0;
        }
    }
}


int is_transpose(int M, int N, int A[N][M], int B[M][N])
{
    int i, j;

    for (i = 0; i < N; i++) {
        for (j = 0; j < M; ++j) {
            if (A[i][j] != B[j][i]) {
                printf("A[%d][%d] != B[%d][%d]",i,j,j,i);
                return 0;
            }
        }
    }
    printf("A==B");
    return 1;
}
void printmt(int row, int col, int array[row][col]){
    for(int i=0;i<row;i++){
        for(int j=0;j<col;j++){
            printf("%d  ", array[i][j]);
        }
        putchar('\n');
    }
    putchar('\n');
}
int main(void){

    int n=32;
    int M=n, N=n, A[N][M], B[M][N],count=1;
    for(int i=0;i<M;i++){
        for(int j=0;j<N;j++){
            A[i][j]=count++;
        }
    }
    memset(B,0,sizeof(B));
    printmt(N,M,A);
    transpose_submit(M, N, A, B);
    is_transpose(M, N, A, B);
    return 0;
}