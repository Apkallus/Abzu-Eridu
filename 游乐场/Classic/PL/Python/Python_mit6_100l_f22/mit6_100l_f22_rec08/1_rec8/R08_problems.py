# RECURSSION PRACTICE
# Problem 1: Write a recursive program to calculate the sum of the positive 
# integers of n+(n-2)+(n-4)... (until and not including n-x =< 0)
# 问题1：编写一个递归程序，计算正整数n+(n-2)+(n-4)...的和（直到且不包括n-x <= 0）
def sum_series(n):
    # 对于偶数
    if n == 0:
        return 0
    # 对于奇数
    elif n == 1:
        return 1
    else:
        return n + sum_series(n - 2)

# testing
# print(sum_series(6))  # 12 
# print(sum_series(10))  # 30 
# print(sum_series(5))  # 9   


##############################################################################
# Problem 2: Write a recursive program to calculate the value of 'a' to the power 'b'
# 问题2：编写一个递归程序来计算'a'的'b'次方
def power(a, b):
    if b == 0:
        return 1
    else:
        return a * power(a, b - 1)

# testing
# print(power(4, 3))  # 64
# print(power(3, 4))  # 81


##############################################################################
# Problem 3: Write a recursive program to calculate the sum of a list of numbers.
# 问题3：编写一个递归程序来计算一组数字的总和。
def list_sum(num_List):
    if num_List == []:
        return 0
    else:
        return num_List[0] + list_sum(num_List[1:])
    
# testing 
# print(list_sum([2, 4, 5, 6, 7]))  # expect 24


##############################################################################
# Problem 4: Write a recurssive program to calculate the nth harmonic number
# 问题4：编写一个递归程序来计算第n个调和数
# 第 n 个调和数 定义为前 n 个正整数的倒数和： Hn = 1/1 + 1/2 + 1/3 + .. + 1/n
def harmonic(n):
    if n == 1:
        return 1
    else:
        return 1/n + harmonic(n-1)

# print(harmonic(3)) # expect 1.83333333333
# print(harmonic(5)) # expect 2.28333333333




# Extra - Problem 5: Write a recursive program to find the greatest common divisor (gcd) 
# of two integers. 
# 附加题 - 问题5：编写一个递归程序来求两个整数的最大公约数（gcd）
# 辗转相除法 
#    被除数         除数      余数
# 除数作为被除数  余数作为除数  新余数
# 当余数为0时，除数即为最大公约数
def gcd(a, b):
    r = a % b
    if r == 0:
        return b
    else:
        return gcd(b, r)


# testing   
print(gcd(5, 4))  # 1 
print(gcd(15, 12))  # 3
print(gcd(12, 12))  # 12


    