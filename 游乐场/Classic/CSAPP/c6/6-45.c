#include<stdio.h>
#include<stdlib.h>
#include <string.h>
void printarray(int dim, int array[dim][dim]);

void trans(int *dst, int *src, int dim){
    int i,j,ii,jj,block,endii,endjj,srcindex;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    int mtblock;
    block=8;
    mtblock=dim-dim%block;
    printf("mtblock%d dim%d\n",mtblock,dim);

    for(i=0;i<mtblock;i+=block){
        for(j=0;j<mtblock;j+=block){

            for(ii=i, endii=i+block; ii<endii; ii++){
                srcindex=ii*dim+j;
                t0=src[srcindex];
                t1=src[srcindex+1];
                t2=src[srcindex+2];
                t3=src[srcindex+3];
                t4=src[srcindex+4];
                t5=src[srcindex+5];
                t6=src[srcindex+6];
                t7=src[srcindex+7];

                dst[j*dim+ii]=t0;
                dst[(j+1)*dim+ii]=t1;
                dst[(j+2)*dim+ii]=t2;
                dst[(j+3)*dim+ii]=t3;
                dst[(j+4)*dim+ii]=t4;
                dst[(j+5)*dim+ii]=t5;
                dst[(j+6)*dim+ii]=t6;
                dst[(j+7)*dim+ii]=t7;
            }  
            printarray(dim,dst);      
        }
    }

    for(int i=0;i<dim;i++){
        for(int j=mtblock;j<dim;j++){
            dst[j*dim+i]=src[i*dim+j];        
        }
    }
    for(int i=mtblock;i<dim;i++){
        for(int j=0;j<dim;j++){
            dst[j*dim+i]=src[i*dim+j];        
        }
    }
    for(int i=mtblock;i<dim;i++){
        for(int j=mtblock;j<dim;j++){
            dst[j*dim+i]=src[i*dim+j];        
        }
    }

}
void printarray(int dim, int array[dim][dim]){
    for(int i=0;i<dim;i++){
        for(int j=0;j<dim;j++){
            printf("%d\t",array[i][j]);
        }
        putchar('\n');
    }
    putchar('\n');
}
void iseq(int dim, int A[dim][dim], int B[dim][dim]){
    int flag=0;
    for(int i=0;i<dim;i++){
        for(int j=0;j<dim;j++){
            if(A[i][j]!=B[j][i]){
                printf("not eq! B[%d][%d]",j,i);
                flag=1;
                break;
            }
        }
        if(flag)break;
    }
    if(!flag)printf("A=t=B");
}
int main(void){

    int dim,*dst,*src;
    dim = 66;
    int A[dim][dim],B[dim][dim],count=1;
    for(int i=0;i<dim;i++){
        for(int j=0;j<dim;j++){
            A[i][j]=count++;
        }
    }
    memset(B,0,sizeof(B));
    printarray(dim,A);
    // printarray(dim,B);
    trans(B[0], A[0], dim);
    printarray(dim,B);
    iseq(dim, A, B);
    return 0;
}