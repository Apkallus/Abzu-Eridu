# 练习 1： 修改你的工资计算程序，使超过 40 小时的工时获得 1.5 倍的时薪。

# Enter Hours: 45
# Enter Rate: 10
# Pay: 475.0

# hours = float(input("Enter Hours: "))
# rate = float(input("Enter Rate: "))
# ext = 0
# if hours > 40:
#     ext = (hours - 40) * 1.5*rate
# pay = 40*rate + ext
# print(f'Pay: {pay:.1f}')


# 练习 2： 使用 try 和 except，以便您的程序能够优雅地处理非数字输入，通过打印一条消息并退出程序。以下展示了该程序的两次执行：

# Enter Hours: 20
# Enter Rate: nine
# Error, please enter numeric input
# Enter Hours: forty
# Error, please enter numeric input

# try:
#     hours = float(input("Enter Hours: "))
#     rate = float(input("Enter Rate: "))
# except:
#     print('Error, please enter numeric input')
#     exit()
# ext = 0
# if hours > 40:
#     ext = (hours - 40) * 1.5*rate
# pay = 40*rate + ext
# print(f'Pay: {pay:.1f}')

# 练习 3： 编写一个程序，提示输入一个 0.0 到 1.0 之间的分数。
# 如果分数超出范围，打印错误消息。如果分数在 0.0 到 1.0 之间，根据以下表格打印等级：

#  Score   Grade
# >= 0.9     A
# >= 0.8     B
# >= 0.7     C
# >= 0.6     D
#  < 0.6     F
# Enter score: 0.95
# A
# Enter score: perfect
# Bad score
# Enter score: 10.0
# Bad score
# Enter score: 0.75
# C
# Enter score: 0.5
# F
# 像上面那样反复运行程序，测试不同的输入值。
# One of the learning objectives of this assignment 
# is to use an elif statement when checking the value of the score.
# 本次作业的学习目标之一是在检查分数值时使用`elif`语句。
##
# try:
#     num = float(input("0.0 ~ 1.0: "))
# except:
#     print('Bad score')
#     exit()
# if num < 0.0 or num > 1.0:
#     print('Bad score')
#     exit()
# else:
#     num_c = int(num * 10)
#     num_dict = {9:'A', 8:'B', 7:'C', 6:'D'}
#     ch = num_dict.get(num_c, 'F')
#     print(ch)
##
# try:
#     num = float(input("0.0 ~ 1.0: "))
# except:
#     print('Bad score')
#     exit()
# if num < 0.0 or num > 1.0:
#     print('Bad score')
#     exit()
# else:
#     ch = 'F'
#     if num >= 0.9:
#         ch = 'A'
#     elif num >= 0.8:
#         ch = 'B'
#     elif num >= 0.7:
#         ch = 'C'
#     elif num >= 0.6:
#         ch = 'D'
#     print(ch)