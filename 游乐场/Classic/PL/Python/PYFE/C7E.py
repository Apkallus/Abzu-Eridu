# 练习 1： 编写一个程序来读取文件并打印文件的内容（逐行），全部大写。执行程序将如下所示：

# python shout.py
# Enter a file name: mbox-short.txt
# FROM STEPHEN.MARQUARD@UCT.AC.ZA SAT JAN  5 09:14:16 2008
# RETURN-PATH: <POSTMASTER@COLLAB.SAKAIPROJECT.ORG>
# RECEIVED: FROM MURDER (MAIL.UMICH.EDU [141.211.14.90])
#      BY FRANKENSTEIN.MAIL.UMICH.EDU (CYRUS V2.3.8) WITH LMTPA;
#      SAT, 05 JAN 2008 09:14:16 -0500
# 您可以从 www.py4e.com/code3/mbox-short.txt 下载文件
# file_name = input('Enter a file name: ')
# file_name = 'mbox-short.txt'
# file_name = 'code3/' + file_name
# fd = open(file_name, 'r')
# for line in fd:
#     print(line.rstrip().upper())
# fd.close()


# 练习 2： 编写一个程序来提示输入文件名，然后通读文件并查找以下格式的行：

# X-DSPAM-Confidence: 0.8475
# 当您遇到以 “X-DSPAM-Confidence：” 开头的行时，请拉开该行以提取该行上的浮点数。
# 对这些行进行计数，然后计算这些行的垃圾邮件置信度值的总和。
# 当您到达文件末尾时，打印出平均垃圾邮件置信度。

# Enter the file name: mbox.txt
# Average spam confidence: 0.894128046745

# Enter the file name: mbox-short.txt
# Average spam confidence: 0.750718518519
# 在 mbox.txt 上测试您的文件并 mbox-short.txt 文件。

## str.partition（sep）
# 在第一次出现 sep 时拆分字符串，并返回一个 3 元组，其中包含分隔符之前的部分、分隔符本身和分隔符之后的部分。
# 如果未找到分隔符，则返回一个包含字符串本身的 3 元组，后跟两个空字符串。

## file_name = input('Enter a file name: ')
# file_name = 'mbox-short.txt'
# file_name = 'code3/' + file_name
# fd = open(file_name, 'r')
# res_list = []
# for line in fd:
#     line_parts = line.partition(':')
#     if line_parts[0] == 'X-DSPAM-Confidence':
#         res_list.append(float(line_parts[2]))
# print(f'Average spam confidence: {sum(res_list)/len(res_list)}')
# fd.close()
##
# file_name = input('Enter a file name: ')
# # file_name = 'mbox-short.txt'
# # file_name = 'code3/' + file_name
# fd = open(file_name, 'r')
# res_sm, res_count = 0, 0
# for line in fd:
#     line_parts = line.partition(':')
#     if line_parts[0] == 'X-DSPAM-Confidence':
#         res_count += 1
#         res_sm += float(line_parts[2])
# print(f'Average spam confidence: {res_sm/res_count}')
# fd.close()

# 练习 3：

# 有时，当程序员感到无聊或想找点乐子时，他们会在他们的程序中添加一个无害的复活节彩蛋 。
# 修改提示用户输入文件名的程序，以便在用户键入确切的文件名 “na na boo boo” 时打印一条有趣的消息。
# 该程序对于存在和不存在的所有其他文件都应该正常运行。以下是该程序的执行示例：

# python egg.py
# Enter the file name: mbox.txt
# There were 1797 subject lines in mbox.txt

# python egg.py
# Enter the file name: missing.tyxt
# File cannot be opened: missing.tyxt

# python egg.py
# Enter the file name: na na boo boo
# NA NA BOO BOO TO YOU - You have been punk'd!

# file_name = input('Enter a file name: ')
files_name = ['mbox.txt', 'missing.tyxt', 'na na boo boo']


def e3(file_name):
    if file_name == 'code3/na na boo boo':
        print('NA NA BOO BOO TO YOU - You have been punk''d!')
        return
    
    try:
        fd = open(file_name, 'r')
    except:
        print(f'File cannot be opened: {file_name}')
        return
    
    count = 0
    for line in fd:
        if line.startswith('Subject:'):
            count += 1

    print(f'There were {count} subject lines in {file_name}')
    fd.close()

# for e in files_name:
#     file_name = 'code3/' + e
#     e3(file_name)