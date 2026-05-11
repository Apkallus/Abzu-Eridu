#include<stdio.h>
int main(void){

    int n;
    char ch;
    scanf("%d",&n);

    switch (n/10)
    {
    case 10:
    case 9:
        ch='A';
        break;
    case 8:
        ch='B';
        break;
    case 7:
        ch='C';
        break;
    case 6:
        ch='D';
        break;
    default:
        ch='E';
        break;
    }
    putchar(ch);
    return 0;
}