#include <stdio.h>
#include <assert.h>

void psume(float a[], float p[], long n){
    long i, end=n-3;
    float val,val2,val3;
    val = p[0] = a[0];
    for(i =1; i<=end ;i+=3){
        val = val + a[i];
        p[i] = val;
        
        val2 = val + a[i+1];
        p[i+1] = val2;
        
        val3= val2 + a[i+2];
        p[i+2] = val3;
        printf("%f,%f,%f\n",val,val2,val3);
    }
    
    for(; i<n ;i++){
        val3 = val3 + a[i];//5-18是元素步长，于是剩余选择x0。而这里是累积，应当选择val3
        p[i] = val3;
        printf("%f\n",val3);
    }
}

void psum1a(float a[], float p[], long n) {
  long i;
  float last_val, val;
  last_val = p[0] = a[0];
  for (i = 1; i < n; i++) {
    val = last_val + a[i];
    p[i] = val;
    last_val = val;
  }
}
#define LOOP 1000
#define LEN  1000
int main(int argc, char* argv[]) {
  float a[5] = { 1, 2, 3, 4, 5 };
  float p[5];
  psum1a(a, p, 5);
  assert(p[4] == 15);

  float q[5];
  psume(a, q, 5);
  assert(q[4] == 15);

  /* for prof */
  for (int i = 0; i < LOOP; i++) {
    float s[LEN];
    float d[LEN];
    psum1a(s, d, LEN);
    psume(s, d, LEN);
  }
  return 0;
}