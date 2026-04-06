# 函数 random 返回一个介于 0.0 和 1.0 之间的随机浮点数（包括 0.0 但不包括 1.0）。
# 每次你调用 random，你都会得到一个长序列中的下一个数。要查看一个示例，运行这个循环：

# import random

# for i in range(10):
#     x = random.random()
#     print(x)
# 练习 1： 在你的系统上运行这个程序，看看你会得到哪些数。多次运行这个程序，看看你会得到哪些数。


def repeat_lyrics():
    print_lyrics()
    print_lyrics()

def print_lyrics():
    print("I'm a lumberjack, and I'm okay.")
    print('I sleep all night and I work all day.')

# repeat_lyrics()

# 这个程序有两个函数定义：print_lyrics 和 repeat_lyrics。函数定义和其他语句一样被执行，但效果是创建函数对象。函数内部的语句直到函数被调用时才执行，函数定义不会产生任何输出。

# 正如你所预料，你必须先创建一个函数才能执行它。换句话说，函数定义必须先被执行，然后才能第一次调用它。

# 练习 2： 将这个程序的最后一行移到顶部，使函数调用出现在定义之前。运行程序并看看你得到什么错误消息。
# NameError: name 'repeat_lyrics' is not defined

# 练习 3： 将函数调用移回底部，并将 print_lyrics 的定义移到 repeat_lyrics 的定义之后。运行这个程序会发生什么？
# 改变定义顺序后，函数调用仍可成功执行。
# 回想在函数中如果有与全局变量同名的本地变量，且先使用后绑定，在本地变量绑定前的使用不是取全局变量，而是报错
# 在python中，似乎只要定义了，与位置无关，是能够找到


# 练习 4：Python 中的“def”关键字有什么作用？
# d

# a) 它是一种俚语，意思是“接下来的代码真的很酷”
# b) 它表示函数的开始
# c) 它表示接下来的缩进代码段将被存储以备后用
# d) b 和 c 都正确
# e) 以上都不对


# 练习 5： 以下 Python 程序会输出什么？
# d

# def fred():
#    print("Zap")

# def jane():
#    print("ABC")

# jane()
# fred()
# jane()
# a) Zap ABC jane fred jane
# b) Zap ABC Zap
# c) ABC Zap jane
# d) ABC Zap ABC
# e) Zap Zap Zap


# 练习 6： 用 加班按1.5倍计算，并创建一个名为 computepay 函数，它接受两个参数 (hours 和 rate).

# Enter Hours: 45
# Enter Rate: 10
# Pay: 475.0

def computepay(hours, rate):
    # hours = float(input("Enter Hours: "))
    # rate = float(input("Enter Rate: "))
    ext = 0
    if hours > 40:
        ext = (hours - 40) * 1.5*rate
    pay = 40*rate + ext
    print(f'Pay: {pay:.1f}')

# computepay(45, 10)


# 练习 7： 使用一个名为 computegrade 的函数重写上一章的评分程序，该函数以分数作为参数并返回一个字符串形式的等级。

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
# 反复运行程序来测试不同的输入值。

def computegrade(num):
    # try:
    #     num = float(input("0.0 ~ 1.0: "))
    # except:
    #     print('Bad score')
    #     exit()
    if type(num) != float:
        return 'Bad score'       

    if num < 0.0 or num > 1.0:
        # print('Bad score')
        # exit()
        return 'Bad score'      
    else:
        ch = 'F'
        if num >= 0.9:
            ch = 'A'
        elif num >= 0.8:
            ch = 'B'
        elif num >= 0.7:
            ch = 'C'
        elif num >= 0.6:
            ch = 'D'
        # print(ch)
        return ch

# a = [0.95, 'perfect', 10.0, 0.75, 0.5]
# for e in a:
#     print(computegrade(e))

# 4.6
def computepay(hours, rate):
    ext = 0
    if hours > 40:
        ext = (hours - 40) * 1.5*rate
    pay = 40*rate + ext
    return pay

hours = float(input("Enter Hours:"))
rate = float(input("Enter Rate:"))
pay = computepay(hours, rate)
print(f"Pay {pay:.2f}")