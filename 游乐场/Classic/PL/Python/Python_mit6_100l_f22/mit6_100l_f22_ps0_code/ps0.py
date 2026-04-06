import numpy
# x = 5
# y = 8
# z = x + y

# a = numpy.log2(z)

# python的input()函数将输入作为字符串
# input()内的字符串作为输入提示
x = input("Enter number x: ")
x = int(x)
y = input("Enter number y: ")
y = int(y)

# print 输出多个对象使用','分隔
print("X**y = ", x**y)
# print 使用'%'进行格式化输出
print("log(x) = %d" %(numpy.log2(x)))