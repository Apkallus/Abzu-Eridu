#include<stdio.h>
#include<stdlib.h>
#include <string.h>
void printarray(int dim, int array[dim][dim]);

void trans(int *G, int dim){
    int i,j,ii,jj,block,endii,endjj,idj,jdi;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    int mtblock;
    block=8;
    mtblock=dim-dim%block;
    printf("mtblock%d dim%d\n",mtblock,dim);

    for(i=0;i<mtblock;i+=block){
        for(j=0;j<mtblock;j+=block){
        // for(j=i;j<mtblock;j+=block){
            //对角线对称,如使用单步则计算一半，即后两个内循环++

            //虽然不同于单矩阵内调换时，如果调换两次则相当于不变，于是必须使用对角线只调换一次
            //这里是两个点计算得到相同的值，没有单矩阵内调换的这种问题
            // 读 读 写
            //但如果直接使用循环展开，则要多读两次，即多一倍
            for(ii=i, endii=i+block; ii<endii; ii++){
                idj=ii*dim+j;
                t0=G[idj];
                t1=G[idj+1];
                t2=G[idj+2];
                t3=G[idj+3];
                t4=G[idj+4];
                t5=G[idj+5];
                t6=G[idj+6];
                t7=G[idj+7];
                
                t0=t0||G[j*dim+ii];
                t1=t1||G[(j+1)*dim+ii];
                t2=t2||G[(j+2)*dim+ii];
                t3=t3||G[(j+3)*dim+ii];
                t4=t4||G[(j+4)*dim+ii];
                t5=t5||G[(j+5)*dim+ii];
                t6=t6||G[(j+6)*dim+ii];
                t7=t7||G[(j+7)*dim+ii];

                G[j*dim+ii]=t0;
                G[(j+1)*dim+ii]=t1;
                G[(j+2)*dim+ii]=t2;
                G[(j+3)*dim+ii]=t3;
                G[(j+4)*dim+ii]=t4;
                G[(j+5)*dim+ii]=t5;
                G[(j+6)*dim+ii]=t6;
                G[(j+7)*dim+ii]=t7;

                // G[idj]=t0;
                // G[idj+1]=t1;
                // G[idj+2]=t2;
                // G[idj+3]=t3;
                // G[idj+4]=t4;
                // G[idj+5]=t5;
                // G[idj+6]=t6;
                // G[idj+7]=t7;
            }  
            // printarray(dim,G);      
        }
    }
    //计算一半，删掉2个的其中1个长边，并将短边按对角线计算
    for(int i=mtblock;i<dim;i++){
        for(int j=0;j<dim;j++){
            idj=i*dim+j;
            jdi=j*dim+i;
            t0=G[idj];
            t0=t0||G[jdi];
            G[jdi]=t0;
            G[idj]=t0;
        }
    }
    for(int i=mtblock;i<dim;i++){
        for(int j=i;j<dim;j++){  
            idj=i*dim+j;
            jdi=j*dim+i;
            t0=G[idj];
            t0=t0||G[jdi];
            G[jdi]=t0;
            G[idj]=t0;   
        }
    }

}

void trans(int *G, int dim){
    int i,j,ii,jj,block,endii,endjj,idj,jdi;
    int t0,t1,t2,t3,t4,t5,t6,t7;
    int mtblock,count;
    block=8;
    mtblock=dim-dim%block;
    printf("mtblock%d dim%d\n",mtblock,dim);
for(i=0;i<mtblock;i+=block){
    for(j=i;j<mtblock;j+=block){
        //关联错误方向的lab
        //同时使用对角线的减半与循环展开
        //将块分为对角线递减块与普通块
        //普通块普通计算，对角线块的减半按照8-7-6-5-4-3-2-1的次数计算
        //使用switch case的无break下落来控制次数
        //由于使用if else 将增加大量判断
        if(i!=j){
            for(ii=i, endii=i+block; ii<endii; ii++){
                idj=ii*dim+j;
                t0=G[idj];
                t1=G[idj+1];
                t2=G[idj+2];
                t3=G[idj+3];
                t4=G[idj+4];
                t5=G[idj+5];
                t6=G[idj+6];
                t7=G[idj+7];
                
                t0=t0||G[j*dim+ii];
                t1=t1||G[(j+1)*dim+ii];
                t2=t2||G[(j+2)*dim+ii];
                t3=t3||G[(j+3)*dim+ii];
                t4=t4||G[(j+4)*dim+ii];
                t5=t5||G[(j+5)*dim+ii];
                t6=t6||G[(j+6)*dim+ii];
                t7=t7||G[(j+7)*dim+ii];

                G[j*dim+ii]=t0;
                G[(j+1)*dim+ii]=t1;
                G[(j+2)*dim+ii]=t2;
                G[(j+3)*dim+ii]=t3;
                G[(j+4)*dim+ii]=t4;
                G[(j+5)*dim+ii]=t5;
                G[(j+6)*dim+ii]=t6;
                G[(j+7)*dim+ii]=t7;

                G[idj]=t0;
                G[idj+1]=t1;
                G[idj+2]=t2;
                G[idj+3]=t3;
                G[idj+4]=t4;
                G[idj+5]=t5;
                G[idj+6]=t6;
                G[idj+7]=t7;
            } 
        }else{//虽然能够与普通块合并，使用条件判断来设置count的值，但不清晰也增加了判断次数
            for(ii=i, endii=i+block; ii<endii; ii++){
                count=ii%block;//0~7
                idj=ii*dim+j;

                switch (count)
                {
                case 0:
                    t0=G[idj];
                case 1:
                    t1=G[idj+1];                     
                case 2:
                    t2=G[idj+2];                
                case 3:
                    t3=G[idj+3];
                case 4:
                    t4=G[idj+4];                    
                case 5:
                    t5=G[idj+5];
                case 6:
                    t6=G[idj+6];
                case 7:
                    t7=G[idj+7];                            
                default:
                    break;
                }

                switch (count)
                {
                case 0:
                    t0=t0||G[j*dim+ii];
                case 1:
                    t1=t1||G[(j+1)*dim+ii];        
                case 2:
                    t2=t2||G[(j+2)*dim+ii];
                case 3:
                    t3=t3||G[(j+3)*dim+ii];
                case 4:
                    t4=t4||G[(j+4)*dim+ii];
                case 5:
                    t5=t5||G[(j+5)*dim+ii];
                case 6:
                    t6=t6||G[(j+6)*dim+ii];
                case 7:
                    t7=t7||G[(j+7)*dim+ii];
                default:
                    break;
                }  
                              
                switch (count)
                {
                case 0:
                    G[j*dim+ii]=t0;                            
                case 1:
                    G[(j+1)*dim+ii]=t1; 
                case 2:
                    G[(j+2)*dim+ii]=t2;
                case 3:                    
                    G[(j+3)*dim+ii]=t3;
                case 4:
                    G[(j+4)*dim+ii]=t4;
                case 5:
                    G[(j+5)*dim+ii]=t5;
                case 6:
                    G[(j+6)*dim+ii]=t6;
                case 7:
                    G[(j+7)*dim+ii]=t7;
                default:
                    break;
                } 

                switch (count)
                {
                case 0:
                    G[idj]=t0;   
                case 1:
                    G[idj+1]=t1;
                case 2:
                    G[idj+2]=t2;
                case 3:
                    G[idj+3]=t3;   
                case 4:
                    G[idj+4]=t4;
                case 5:
                    G[idj+5]=t5;
                case 6:
                    G[idj+6]=t6;        
                case 7:
                    G[idj+7]=t7;                           
                default:
                    break;
                }
            } 
        }
 
        // printarray(dim,G);      
    }
}
    //计算一半，删掉2个的其中1个长边，并将短边按对角线计算
    for(int i=mtblock;i<dim;i++){
        for(int j=0;j<dim;j++){
            idj=i*dim+j;
            jdi=j*dim+i;
            t0=G[idj];
            t0=t0||G[jdi];
            G[jdi]=t0;
            G[idj]=t0;
        }
    }
    for(int i=mtblock;i<dim;i++){
        for(int j=i;j<dim;j++){  
            idj=i*dim+j;
            jdi=j*dim+i;
            t0=G[idj];
            t0=t0||G[jdi];
            G[jdi]=t0;
            G[idj]=t0;   
        }
    }

}
// void printarray(int dim, int array[dim][dim]){
//     for(int i=0;i<dim;i++){
//         for(int j=0;j<dim;j++){
//             printf("%d\t",array[i][j]);
//         }
//         putchar('\n');
//     }
//     putchar('\n');
// }
// void iseq(int dim, int A[dim][dim], int B[dim][dim]){
//     int flag=0;
//     for(int i=0;i<dim;i++){
//         for(int j=0;j<dim;j++){
//             if(A[i][j]!=B[j][i]){
//                 printf("not eq! B[%d][%d]",j,i);
//                 flag=1;
//                 break;
//             }
//         }
//         if(flag)break;
//     }
//     if(!flag)printf("A=t=B");
// }
int main(void){

    // int dim,*dst,*src;
    // dim = 66;
    // int A[dim][dim],B[dim][dim],count=1;
    // for(int i=0;i<dim;i++){
    //     for(int j=0;j<dim;j++){
    //         A[i][j]=count++;
    //     }
    // }
    // memset(B,0,sizeof(B));
    // printarray(dim,A);
    // // printarray(dim,B);
    // trans(B[0], A[0], dim);
    // printarray(dim,B);
    // iseq(dim, A, B);
    return 0;
}