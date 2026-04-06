# 练习 1： 编写一个名为 chop 获取列表并对其进行修改，
# 删除第一个和最后一个元素，并返回 None。
# 然后编写一个名为 middle 的函数，该函数接受一个列表并返回一个新列表，
# 该列表包含除第一个和最后一个元素之外的所有元素。

def e1(p_list):
    del(p_list[0])
    del(p_list[-1])

def middle(p_list):
    return p_list[1:-1]

# a = [1,2,3,4,5]
# b = a[:]
# e1(b)
# print(b)
# print(middle(a))



# fhand = open('mbox-short.txt')
# count = 0
# for line in fhand:
#     words = line.split()
#     # print('Debug:', words)
#     if len(words) == 0 : continue
#     if words[0] != 'From' : continue
#     print(words[2])

# 练习 2： 找出上述程序的哪一行仍然没有得到适当的保护。
#     看看你是否可以构造一个导致程序失败的文本文件，然后修改该程序以正确保护该行并测试它以确保它处理你的新文本文件。

# 练习 3： 重写上面示例中的保护者代码，
#     没有两个 if 语句。相反，请将 or 逻辑运算符与单个 if 语句结合使用复合逻辑表达式。

# # E2
# try:
#     fhand = open('mbox-short.txt')
# except:
#     print('file name error')
#     exit()
# count = 0
# for line in fhand:
#     words = line.split()
#     # print('Debug:', words)
#     if len(words) == 0 : continue
#     if words[0] != 'From' : continue

#     if len(words) >= 3:
#         print(words[2])

# # E3
# fhand = open('mbox-short.txt')
# count = 0
# for line in fhand:
#     words = line.split()
#     # print('Debug:', words)
#     if len(words) == 0 or words[0] != 'From' : continue
#     print(words[2])


# 练习 4：查找文件中的所有唯一单词

# 莎士比亚在他的作品中使用了超过 20,000 个单词。
# 但是你怎么确定呢？您将如何列出莎士比亚使用的所有单词列表？
# 您会下载他的所有作品，阅读并手动跟踪所有独特的单词吗？

# 让我们使用 Python 来实现这一点。列出所有唯一单词， 
# 按字母顺序排序，存储在文件中 romeo.txt 包含莎士比亚作品的子集。

# 要开始使用，请下载文件 www.py4e.com/code3/romeo.txt 的副本。
# 创建一个唯一单词列表，其中包含最终结果。
# 编写一个程序以打开文件 romeo.txt 并读取该行 按线。
# 对于每一行，使用 split 函数。对于每个单词，检查该单词是否已经在唯一单词列表中。
# 如果该单词不在唯一单词列表中，请将其添加到列表中。
# 程序完成后，按字母顺序对唯一单词列表进行排序和打印。

# Enter file: romeo.txt
# ['Arise', 'But', 'It', 'Juliet', 'Who', 'already',
# 'and', 'breaks', 'east', 'envious', 'fair', 'grief',
# 'is', 'kill', 'light', 'moon', 'pale', 'sick', 'soft',
# 'sun', 'the', 'through', 'what', 'window',
# 'with', 'yonder']
# fd = open("code3/romeo.txt")
# unt_list = []
# for line in fd:
#     words_line = line.split()
#     for word in words_line:
#         if word not in unt_list:
#             unt_list.append(word)
#     ##! 使用列表推导式导致重复单词!##unt_list += [word for word in words_line if word not in unt_list]
# fd.close()
# unt_list.sort()
# print(unt_list)


# 练习 5：极简电子邮件客户端。

# MBOX（邮箱）是一种流行的文件格式，用于存储和共享电子邮件集合。
# 早期的电子邮件服务器和桌面应用程序都使用此功能。
# 无需过多细节，MBOX 是一个文本文件，可以连续存储电子邮件。
# 电子邮件由以 From 开头的特殊行分隔（注意空格）。
# 重要的是，以 From： 开头的行（注意冒号）描述电子邮件本身，不充当分隔符。
# 想象一下，你编写了一个极简的电子邮件应用程序，
# 它列出了用户收件箱中发件人的电子邮件，并计算了电子邮件的数量。

# 编写一个程序来读取邮箱数据，当您找到以 “From” 开头的行时，您将使用 split 函数将行拆分为单词。
# 我们对消息的发送者感兴趣，这是 From 行上的第二个单词。

# From stephen.marquard@uct.ac.za Sat Jan 5 09:14:16 2008
# 您将解析 From 行并打印出每个 From 行的第二个单词，
# 然后您还将计算 From（不是 From：）行的数量，并在最后打印出一个计数。
# 这是一个很好的示例输出，其中删除了几行：

# python fromcount.py
# Enter a file name: mbox-short.txt
# stephen.marquard@uct.ac.za
# louis@media.berkeley.edu
# zqian@umich.edu

# [...some output removed...]

# ray@media.berkeley.edu
# cwen@iupui.edu
# cwen@iupui.edu
# cwen@iupui.edu
# There were 27 lines in the file with From as the first word

# fd = open("code3/mbox-short.txt")
# count = 0
# for line in fd:
#     words = line.split()
#     if len(words) < 1 or words[0] != 'From':
#         continue
#     count += 1
#     if len(words) >= 2:
#         print(words[1])
# print(f'There were {count} lines in the file with From as the first word')


# 练习 6：

# 重写提示用户输入数字列表并在用户输入 “done” 时打印出数字的最大值和最小值的程序。
# 编写程序以存储用户在列表中输入的数字，
# 并使用 max（） 和 min（） 函数来计算循环后的最大和最小数字 完成。

# Enter a number: 6
# Enter a number: 2
# Enter a number: 9
# Enter a number: 3
# Enter a number: 5
# Enter a number: done
# Maximum: 9.0
# Minimum: 2.0

# numbers = []
# while True:
#     usr_input = input('Enter a number: ')
#     if usr_input == 'done': break
#     num = int(usr_input)
#     numbers.append(num)
# print(f'Maximum: {max(numbers):.1f}\nMinimum: {min(numbers):.1f}')