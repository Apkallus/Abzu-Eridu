#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void *basic_memset(void *s, int c, size_t n){
    size_t cnt = 0;
    unsigned char *schar = s;
    while(cnt < n){
        *schar++ = (unsigned char)c;
        cnt++;
    }
    return s;
}

void *effective_memset(void *s, int c, size_t n){
    unsigned char ch = (unsigned char)c;
    unsigned long long mask = 0;
    size_t cnt;
    size_t step = sizeof(unsigned long long);// long 在windows为4字节

    for(cnt = 1; cnt <= step; cnt ++){
        mask=(mask<<8)+ch;//位移符号优先级低，需括号
    }
	
    unsigned char *schar = (unsigned char *)s;
    for(cnt = 0; (size_t)schar % step && cnt < n; cnt++, schar++){
        //如果地址不是倍数且在n范围内则继续循环
        *schar = ch;
    }
    n = n - cnt;
    size_t end = n - step;//无符号减法
    unsigned long long *slong = (unsigned long long *)schar;
    if(end < n){//如果无符号减法没有溢出  
        for(cnt = 0; cnt <= end; cnt+=step, slong++){
            *slong = mask;
        }
    }

    schar = (unsigned char *)slong;
    for(; cnt < n; cnt++, schar++){
        *schar = ch;
    }
    return s;
}

int main(void) {
    size_t space = sizeof(char) * 65537;

    // careful! malloc SIZE_MAX size memory will make sys slow
    // or crash down
    // size_t space = SIZE_MAX;
  
    void* basic_space = malloc(space);
    void* effective_space = malloc(space);
  
    int basic_fill = 0xFF;
    int effective_fill = ~0;
  
    basic_memset(basic_space, basic_fill, space);
    effective_memset(effective_space, effective_fill, space);
    assert(memcmp(basic_space, effective_space, space) == 0);
  
    free(basic_space);
    free(effective_space);
    return 0;
  }
  
  
