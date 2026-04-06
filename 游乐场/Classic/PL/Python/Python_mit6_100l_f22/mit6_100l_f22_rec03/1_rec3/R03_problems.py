# Problem 1 - Bisection Search Practise
# Write a program using bisection search to find the forth root of a number inputted by the 
# user. Print the forth root calculated with max error of 0.01. 
# 问题1 - 二分查找练习
# 编写一个程序，使用二分查找法计算用户输入数字的四次方根。输出计算得到的四次方根，最大误差不超过0.01。
# x = float(input("Using bisection search calculate the forth root of: " ))
# epsilon = 0.01
# low = 0
# high = max(1, x)
# ans = (low + high) / 2
# while abs(ans**4 - x) > epsilon:
#     if ans**4 > x:
#         high = ans
#     else:
#         low = ans
#     ans = (low + high) / 2
    



# Problem 2 - Functions 
# Write a Python function to check whether a number falls in a given range. 
# 编写一个Python函数来检查一个数字是否落在给定范围内。
# def check_in_range(num, start, end):
## 也可直接比较端点的大小
#     if num in range(start, end+1):
#         res_flag = True
#     else:
#         res_flag = False
#     return res_flag

# print(check_in_range(3, 1, 5))
# print(check_in_range(3, 5, 7))  

# Problem 3 - Functions 
# Write a Python function to check whether a number is perfect or not.
# (In number theory, a perfect number is a positive integer that is equal 
# to the sum of its proper positive divisors, excluding the number itself).
# 编写一个Python函数来检查一个数是否为完美数。
# （在数论中，完美数是指一个正整数等于其所有真正因子之和，不包括该数本身）。
# def perfect_number(num):
#     sum = 0
#     for i in range(1,num):
#         if num % i == 0:
#             sum += i
#     return num == sum

# print(perfect_number(6))
# print(perfect_number(28))
# print(perfect_number(50))


# Problem 4 - Approximation Algorithm (see Lecture 5 slides for similar problem)
# Write an approximation algorithm to calculate the forth root of some 
# number inputted by the user. 
# Print the result and the number of iterations required to reach that result. 
# The program should not accept negative numbers. Initial parameters epsilon 
# (i.e. accuracy), initial guess, increment and num_guesses are defined below.
# 问题4 - 近似算法（参见第5讲幻灯片中的类似问题）
# 编写一个近似算法来计算用户输入的某个数的四次方根。
# 打印结果以及达到该结果所需的迭代次数。
# 程序不应接受负数。初始参数epsilon（即精度）、初始猜测值、增量以及猜测次数定义如下。

# example initial parameters
epsilon = 0.01
ans = 0.0
increment = 0.001
num_guesses = 0

num = float(input("input num"))
if num >= 0:
    while abs(ans**4 - num) > epsilon and ans**4 < num:
        ans += increment
        num_guesses += 1
    
    if abs(ans**4 - num) > epsilon:
        print(f"not find, last one is: ans={ans}, num_guesses={num_guesses}")
    else:
        print(f"find: ans={ans}, num_guesses={num_guesses}")        
else:
    print("please input pos number")
