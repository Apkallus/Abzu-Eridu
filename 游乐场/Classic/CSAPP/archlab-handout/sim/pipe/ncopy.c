#include <stdio.h>

typedef word_t word_t;

word_t src[8], dst[8];

/* $begin ncopy */
/*
 * ncopy - copy src to dst, returning number of positive ints
 * contained in src array.
 */
word_t ncopy(word_t *src, word_t *dst, word_t len)
{
    word_t count = 0;
    word_t val;

    while (len > 0) {
        val = *src++;
        *dst++ = val;
        if (val > 0)
            count++;
        len--;
    }
    return count;
}
/* $end ncopy */

/* 第五章 5.8循环展开
n个元素 循环界限为<n-(k-1)
k个循环展开因子

count=0
k=7
limit = n-k
while(limit>=0){

    val1 = 0(src)
    val2 = 8(src)
    ...
    val6 = 40(src)
    val7 = 48(src)
    
    0(dst) = val1
    8(dst) = val2
    ...
    40(dst) = val6
    48(dst) = val7
   
    if (val1 > 0)
        count++
    ...
    if (val7 > 0)
        count++

    blimit-=7
}
limit=-limit
while(limit>0){
    val1 = 0(src)
    0(dst) = val1

    if (val1 > 0)
        count++
    blimit--
}

*/
int main()
{
    word_t i, count;

    for (i=0; i<8; i++)
	src[i]= i+1;
    count = ncopy(src, dst, 8);
    printf ("count=%d\n", count);
    exit(0);
}


