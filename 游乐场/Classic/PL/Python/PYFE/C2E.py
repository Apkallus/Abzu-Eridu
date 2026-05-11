# 练习 2： 编写一个程序，使用 input 提示用户输入他们的名字，然后欢迎他们。

# Enter your name: Chuck
# Hello Chuck

# name = input("Enter your name: ")
# print(f'Hello {name}')


# 练习 3： 编写一个程序，提示用户输入工作小时数和每小时工资率，以计算总工资。

# Enter Hours: 35
# Enter Rate: 2.75
# Pay: 96.25
# 目前我们不必担心确保我们的工资在十进制点后正好有两位数字。如果你愿意，你可以使用内置的 Python round 函数来将计算结果正确地四舍五入到两位小数。

# hours = float(input("Enter Hours: "))
# rate = float(input("Enter Rate: "))
# pay = hours*rate
# print(f'Pay: {pay:.2f}')

# 练习 4： 假设我们执行以下赋值语句：

# width = 17
# height = 12.0
# 对于以下每个表达式，写出表达式的值及其类型（表达式值的类型）。

# width//2
# 8 int

# width/2.0
# 8.5 float

# height/3
# 4.0 float

# 1 + 2 * 5
# 11 int

# 使用 Python 解释器检查你的答案。

# 练习 5： 编写一个程序，提示用户输入摄氏温度，将温度转换为华氏温度，并打印出转换后的温度。
# F = C × (9/5) + 32
# c = float(input("c: "))
# f = c * (9/5) + 32
# print(f'f: {f:.2f}')