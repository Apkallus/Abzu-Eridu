# 练习 1： 写一个 while 循环，从字符串的最后一个字符开始，
#     反向工作到第一个字符，每个字母单独打印一行，但顺序相反。
# e1_str = 'abcdefg'
# index = len(e1_str) - 1
# while index >= 0:
#     print(e1_str[index])
#     index -= 1

# 练习 2： 已知 fruit 是一个字符串，fruit[:] 表示什么？
# fruitn绑定字符串的完整副本


# 以下程序统计字符串中字母“a”出现的次数：

# word = 'banana'
# count = 0
# for letter in word:
#     if letter == 'a':
#         count = count + 1
# print(count)
# 这个程序展示了另一种计算模式，称为 计数器 。
# 变量 count 被初始化为 0 每次找到“a”时就会递增。
# 当循环退出时， count 包含结果：总共找到的“a”的数量。

# 练习 3： 将这段代码封装在一个名为 count 的函数中，并使其通用化，以便它接受字符串和字母作为参数。
def count(word):
    count = 0
    for letter in word:
        if letter == 'a':
            count = count + 1
    print(count)
    return count

word = 'banana'
# count(word)



# 练习 4： 有一个名为 count 的字符串方法，它与上一个练习中的函数类似。请查阅该方法的文档：

# https://docs.python.org/library/stdtypes.html#string-methods

# 编写一个调用语句，计算字母 a 在“banana”中出现的次数。
word = 'banana'
# print(word.count('a'))


# 练习 5： 字符串切片

# 取以下存储字符串的 Python 代码：

e5_str = 'X-DSPAM-Confidence: 0.8475 '

# 使用 find 和字符串切片提取冒号字符后的字符串部分，然后使用 float 将提取的字符串转换为浮点数的函数 数字。
float_str = e5_str[e5_str.find(':')+1 :]
print(f'>{float_str}<') 
print(float(float_str))
## 即使字符串中有空格，float()转换仍可成功运行
## print(int(' 6 \n \t'))


# 练习 6： 字符串方法

# 阅读字符串方法的文档

# https://docs.python.org/library/stdtypes.html#string-methods.

# 你可能需要尝试一些方法来确保你理解它们的工作方式。 strip 和 replace 特别有用。

# 文档使用了一种可能令人困惑的语法。例如，在 find(sub[, start[, end]]) 中，括号表示可选参数。
# 所以 sub 是必需的，但 start 是可选的，如果你包含 start，那么 end 也是可选的。
