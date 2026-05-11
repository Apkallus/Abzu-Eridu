# Assume you are given a variable named number (has a numerical value). 
# Write a piece of Python code that prints out one of the following strings: 
# 假设您有一个名为 number 的变量（具有数值）。
# 编写一段 Python 代码，打印出以下字符串之一： 

# positive if the variable number is positive
# 如果变量数为正数， 则为 positive
# negative if the variable number is negative
# 如果变量 number 为负数， 则为 negative
# zero if the variable number is equal to zero
# 如果变量 number 等于零， 则为零

number = int(input("input a number: "))

if number > 0:
    outstr = 'positive'
elif number < 0:
    outstr = 'negative'
else:
    outstr = 'zero'

print(f"input number {number} is {outstr}")