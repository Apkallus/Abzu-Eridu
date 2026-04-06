/* 
 * CS:APP Data Lab 
 * 
 * <Please put your name and userid here>
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting if the shift amount
     is less than 0 or greater than 31.


EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implement floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants. You can use any arithmetic,
logical, or comparison operations on int or unsigned data.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operations (integer, logical,
     or comparison) that you are allowed to use for your implementation
     of the function.  The max operator count is checked by dlc.
     Note that assignment ('=') is not counted; you may use as many of
     these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
//1
/* 
 * bitXor - x^y using only ~ and & 
 *   Example: bitXor(4, 5) = 1
 *   Legal ops: ~ &
 *   Max ops: 14
 *   Rating: 1
 */
int bitXor(int x, int y) {//完成
/* 重新解释
  int xo=x&~y;//x独有
  int yo=y&~x;//y独有
  int nxo=~xo;//非x独有
  int nyo=~yo;//非y独有
  int nxy=nxo&nyo;//x与y都有
  int res=~nxy;//x与y独有
*/
  int bothhave=x&y;//都有
  int bothnothave=(~x)&(~y);//都无
  int nbh=~bothhave;//不是都有
  int nbnh=~bothnothave;//不是都无
  int res=nbh&nbnh;//不同时有或无
  return res;
}
/* 
 * tmin - return minimum two's complement integer 
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 */
int tmin(void) {//完成

  return 1<<31;//2的31次幂 将1左移31位

}
//2
/*
 * isTmax - returns 1 if x is the maximum, two's complement number,
 *     and 0 otherwise 
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 10
 *   Rating: 1
 */
int isTmax(int x) {//完成#
/*不能使用位移与减号 
  int tmax=(1<<31)-1;//2的31次幂-2的0次幂 得到从30位到0位的全1位向量
  return !(x^tmax);
*/
/*
//无法通过————但btest的参数在devc++返回正确
  int isoverflow=!(x+x+2);//如果x是tmax tmax+1=tmin tmin+tmin=0
  int isxneg1=!!(x^(~1+1));
  return isoverflow&isxneg1;//排除x=-1
*/
//与无法通过的函数使用相似思路，上面的使用两个tmin溢出，下面的使用tmin+tmax=-1
/*  int istmin=x+1;//tmax+1=tmin
  int res=x+istmin;//res=-1
  int neg1=~1+1;
  int isresneg1=!(res^neg1);
  int isxneg1=!!(x^neg1);
  return isresneg1&isxneg1;
*/
//相似思路2，除-1外，x+1是否等于~x
//在于用能够简单表示的特殊值来判断
  int istmin1=x+1;
  int istmin2=~x;
  int isxneg1=!!(x^(~0));
  return !(istmin1^istmin2)&isxneg1;
}
/* 
 * allOddBits - return 1 if all odd-numbered bits in word set to 1
 *   where bits are numbered from 0 (least significant) to 31 (most significant)
 *   Examples allOddBits(0xFFFFFFFD) = 0, allOddBits(0xAAAAAAAA) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
int allOddBits(int x) {//完成
  //10101010 AA
  int mask=0xAA+(0xAA<<8)+(0xAA<<16)+(0xAA<<24);//位移并累加AA创造偶数位全为1的mask
  return !((x&mask)^mask);//mask判断x偶数位是否为1，如全部匹配 &后将等于mask
}
/* 
 * negate - return -x 
 *   Example: negate(1) = -1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
int negate(int x) {//完成
  return ~x+1;//一个数的加法逆元等于这个数的补+1
}
//3
/* 
 * isAsciiDigit - return 1 if 0x30 <= x <= 0x39 (ASCII codes for characters '0' to '9')
 *   Example: isAsciiDigit(0x35) = 1.
 *            isAsciiDigit(0x3a) = 0.
 *            isAsciiDigit(0x05) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 3
 */
int isAsciiDigit(int x) {//完成
/*不能使用减号
  int x39=((x-0x3A)>>31)&1;//如果x小于0x3A，即小于等于0x39，值为负，位移31位取符号，得全1,&1取值1或0
  int x30=!((x-0x30)>>31);//如果x大于等于0x30，值为非负，位移得全0,!0=1
  return x39&x30; 
*/
  int x39=((x+~0x3A+1)>>31)&1;//如果x小于0x3A，即小于等于0x39，值为负，位移31位取符号，得全1,&1取值1或0
  int x30=!((x+~0x30+1)>>31);//如果x大于等于0x30，值为非负，位移得全0,!0=1
  return x39&x30;
  }
/* 
 * conditional - same as x ? y : z 
 *   Example: conditional(2,4,5) = 4
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 16
 *   Rating: 3
 */
int conditional(int x, int y, int z) {//完成
  int zerox=!x;//当x非零zerox=0，当x为零zerox=1
  int masky=(!zerox<<31)>>31;//当x非零 masky全1
  int maskz=(zerox<<31)>>31;//当x为零 maskz全1
  int xy=y&masky;//当x非零 xy=y 当x为零 xy=0
  int xz=z&maskz;//当x非零 xz=0 当x为零 xz=z
  return xy|xz;
}
/* 
 * isLessOrEqual - if x <= y  then return 1, else return 0 
 *   Example: isLessOrEqual(4,5) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
int isLessOrEqual(int x, int y) {//完成#
/*  无法通过————缺乏对不同情况的处理而只是排除tmin
  return !((1<<31)^x)|((!((y+~x+1)>>31))&!!((1<<31)^y));
  // 差值的符号位右移，若非负则全0 若为负则全1。但对于tmin，~tmin+1仍为本身，即使大于tmin值仍为负，那么排除tmin
*/
  //
  int xneg=x>>31;
  int yneg=y>>31;//如果x y为负 则x与y neg值为1
  int xorflag=xneg^yneg;
  int sameflag=(!xorflag)&!((y+~x+1)>>31);//相同符号时均为y-x为正时y大
  int diftflag=xorflag&!yneg;//不同符号时只在y为正时
  return sameflag|diftflag;
}
//4
/* 
 * logicalNeg - implement the ! operator, using all of 
 *              the legal operators except !
 *   Examples: logicalNeg(3) = 0, logicalNeg(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4 
 */
int logicalNeg(int x) {
  //如果为负数
  int isneg=x>>31;
  //如果为非负数
  int tmax=~(1<<31);
  int ispos=(x+tmax)>>31;
  //合并两种情况，取最低位异或1取反
  return ((isneg|ispos)&1)^1;
}
/* howManyBits - return the minimum number of bits required to represent x in
 *             two's complement
 *  Examples: howManyBits(12) = 5           01001
 *            howManyBits(298) = 10    0100101010
 *            howManyBits(-5) = 4            1011
 *            howManyBits(0)  = 1               0
 *            howManyBits(-1) = 1               1
 *            howManyBits(0x80000000) = 32
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 90
 *  Rating: 4
 */
int howManyBits(int x) {//完成
  /*二分左移再右移高位后如果值变化，则至少有二分右边的低位 16-8-4-2-1
  向左位移增加是单向的，
  于是在拥有右侧低位时累计并右移来去掉已经计数的位，从而继续判断剩余高位*/
  int count=1;
  int neg1=~0;
  int lm16,lm24,lm28,lm30,lm31;
  int ct16,ct24,ct28,ct30,ct31;
  int is16,is24,is28,is30,is31;

  lm16=x<<16>>16;
  ct16=16;
  is16=(!(lm16^x)+neg1)&ct16;
  count=count+is16;
  x=x>>is16;

  lm24=x<<24>>24;
  ct24=8;
  is24=(!(lm24^x)+neg1)&ct24;
  count=count+is24;
  x=x>>is24;

  lm28=x<<28>>28;
  ct28=4;
  is28=(!(lm28^x)+neg1)&ct28;
  count=count+is28;
  x=x>>is28;

  lm30=x<<30>>30;
  ct30=2;
  is30=(!(lm30^x)+neg1)&ct30;
  count=count+is30;
  x=x>>is30;

  lm31=x<<31>>31;
  ct31=1;
  is31=(!(lm31^x)+neg1)&ct31;
  count=count+is31;

  return count;
}
//float
/* 
 * floatScale2 - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
unsigned floatScale2(unsigned uf) {//完成
/*
  传递值与返回值都作为浮点数解释
*/
  unsigned res;  
  unsigned s=((uf>>31)&1)<<31;
  unsigned exp=((uf>>23)&0xFF);
  unsigned isspecial=exp^0xFF;//检查是否为特殊值
  unsigned tmin=1<<31;
  unsigned expp=1<<23;
  unsigned f=uf&~(tmin-expp+tmin);
  exp=exp<<23;

  if(isspecial){//如果不是阶码全1的特殊值
    //如果是规格化浮点数，计算时增加小数位隐含的整数1
    if(exp){
      f=f+expp;
    }
    //阶码无需对齐，计算小数位
    f=f+f;
    if(exp){//规格进位后右移小数位并增加阶码
      f=(f>>1)-expp;
      exp=exp+expp;
    }else{//非规格
      if(f>>23){//非规格若从<1进位到>=1则转为规格化
        f=f-expp;
        exp=exp+expp;
      }
    }
    res=s|exp|f;
  }else{//如果是特殊值
    res=uf;
  }


  return res;
}
/* 
 * floatFloat2Int - Return bit-level equivalent of expression (int) f
 *   for floating point argument f.
 *   Argument is passed as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point value.
 *   Anything out of range (including NaN and infinity) should return
 *   0x80000000u.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */

int floatFloat2Int(unsigned uf) {//完成
  //关联2-96
  // 强制类型转换float到int
  //uf==0x3f800000  res=0x1;
  //uf==0xbf800000  res=-1 0xffffffff
  //uf==0x7f000000  res=0x80000000;
  int res,E,Bias=127;  
  int s=((uf>>31)&1)<<31;
  int exp=((uf>>23)&0xFF);
  int isspecial=exp^0xFF;//检查是否为特殊值
  int tmin=1<<31;
  int expp=1<<23;
  int f=uf&~(tmin-expp+tmin);

  if(isspecial){//如果不是阶码全1的特殊值
    if(exp){//如果是规格化浮点数
      f=f+expp;//M+1
      E=exp-Bias;
      if(E>=0){
        if(E<=23){//从整数1的位右移来确定能够作为整数保留的小数位
          f=f>>(23-E);//E相对于23表示能够保留的整数位数量
          s=s>>(30-E);//符号扩展到数前一位
          res=s|f;
        }else if(E<=30){//左移来确定要增加多少个0
          f=f<<(E-23);
          s=s>>(30-E);
          res=s|f;
        }else{
          res=0x80000000u;
        }
      }else{
        res=0;
      }
    }else{//如果是非规格化
      res=0;
    }
  }else{//如果是特殊值
    res=0x80000000u;
  }
  return res;
}
/* 
 * floatPower2 - Return bit-level equivalent of the expression 2.0^x
 *   (2.0 raised to the power x) for any 32-bit integer x.
 *
 *   The unsigned value that is returned should have the identical bit
 *   representation as the single-precision floating-point number 2.0^x.
 *   If the result is too small to be represented as a denorm, return
 *   0. If too large, return +INF.
 * 
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. Also if, while 
 *   Max ops: 30 
 *   Rating: 4
 */
unsigned floatPower2(int x) {//完成
  //2的x次幂
  
  int Bias=127;
  int ME=-23;
  int DNE=1-Bias+ME;//最小非规格化负幂+小数负幂 最小非规格化数阶码全0 小数位00···1 同时使用阶码负幂与小数位负幂
  int NNE=0xFF-1-Bias;//最大规格化E
  int NNexp,DNexp;
  unsigned res;

  if(x<DNE){
    res=0;
  }else if(x>NNE){
    res=0xFF<<23;//浮点正无穷
  }else{
    if(x>=1-Bias){//如果在规格化范围 最小规格化阶码00···1 小数位全0 只使用阶码的负幂 由于其隐含的1
      NNexp=x+Bias;
      res=NNexp<<23;
    }else{//如果是非规格化 btest未使用 阶码位为0，使用小数位表示负幂， 关联2-90
      res=1<<(x-DNE);
    }
  }
    return res;
}
