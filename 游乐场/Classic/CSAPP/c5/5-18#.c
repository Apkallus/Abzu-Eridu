#include <stdio.h>
#include <assert.h>
double polye(double a[], double x, long degree){
    long i;
    double result;
    long accn = 3;//积累变量数量
    long ee = 3;//每个积累变量所累积的元素数量
    long accn2 = accn *2;
    long step = ee * accn;
    long end = degree-step;
    double acc0,acc1,acc2;
    acc0=acc1=acc2=0;
    double x0=1, x1=x, x2=x*x;
    double xs=1,xe=1;
    long i2,i3;
    for(i=1;i<=step;i++){//xs为每次循环时幂的步长
        xs*=x;
    }
    for(i=1;i<=accn;i++){//xe由累积变量数量计算出的每个累积变量的元素提出的x的幂的间隔 
        xe*=x;
    }
    for(i=0;i<=end;i+=step){
        i2=i+accn;//由累积变量数量计算出的每个累计变量元素数组a的角标
        i3=i+accn2;
//      acc0+= x0*(a[i]+a[i2]*x2);
        acc0+= x0*(a[i]+xe*(a[i2]+a[i3]*xe));
        acc1+= x1*(a[i+1]+xe*(a[i2+1]+a[i3+1]*xe));
        acc2+= x2*(a[i+2]+xe*(a[i2+2]+a[i3+2]*xe));
        x0*=xs;
        x1*=xs;
        // 如果每个累积变量内的元素相邻是否有更高性能？
        // 或许缓存能够存放所有单次循环的内存数据而无差别，或许被覆盖再次读取
        // 或许即使能够存放到缓存中，但有对单步的优化或单次取一段连续数据而使得相邻更高效
        // 由此，在单个累积变量中使用步长为1的模式能够确保高效，而步长>1不一定
    }    
    for(;i<=degree;i++){//这里是从0~n 于是应当包括n
        acc0+= x0*a[i];
        x0*=x;
    } 
    result=acc0+acc1+acc2;
    printf("polye = %lf\n",result);
    return result;
}

double poly(double a[], double x, long degree) {
  long i;
  double result = a[0];
  double xpwr = x;
  for (i = 1; i <= degree; i++) {
    result += a[i] * xpwr;
    xpwr = x * xpwr;
  }
  printf("poly = %lf\n",result);
  return result;
}

double polyh(double a[], double x, long degree) {
  long i;
  double result = a[degree];
  for (i = degree-1; i >= 0; i--) {
    result = a[i] + x*result;
  }  
  printf("polyh = %lf\n",result);
  return result;
}

#define LOOP 1000
#define LEN 1000

int main(int argc, char* argv[]) {
    double a[10 + 1] = { 0, 1, 2, 3, 4, 5,
                            6, 7, 8, 9, 10};
    double x = 2;
    long degree = 10;

//    assert(poly(a, x, degree) == 2+4+8+16+32+(2+4+8+16+32)*32);
    assert(poly(a, x, degree) == polye(a, x, degree));
//    assert(polye(a, x, degree) == 2+4+8+16+32+(2+4+8+16+32)*32);
    
    return 0;
}
