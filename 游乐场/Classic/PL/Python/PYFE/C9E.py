# 练习 1：下载该文件的副本

# www.py4e.com/code3/words.txt

# 编写一个程序，读取 words.txt 文件中的单词，并将它们作为键存储在一个字典中。
# 值是什么并不重要。然后，您可以使用  in  运算符作为快速检查字符串是否在字典中的方法。

# fd = open('code3/words.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     for word in words:
#         res_dict[word] = 0


# 练习 2： 编写一个程序，按提交完成的星期几对每封邮件进行分类。
# 为此，请查找以 “From” 开头的行，然后查找第三个单词，并保留一周中每一天的运行计数。
# 在程序结束时，打印出字典的内容（顺序无关紧要）。

# 示例行：

# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
# 示例执行：

# python dow.py
# Enter a file name: mbox-short.txt
# {'Fri': 20, 'Thu': 6, 'Sat': 1}
# fd = open('code3/mbox-short.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     if len(words) < 3 or words[0] != 'From':
#         continue
#     week = words[2]
#     res_dict[week] = res_dict.get(week, 0) + 1
# print(res_dict)


# 练习 3： 编写一个程序来读取邮件日志，使用字典构建直方图来计算来自每个电子邮件地址的邮件数量，然后打印字典。

# Enter file name: mbox-short.txt
# {'gopal.ramasammycook@gmail.com': 1, 'louis@media.berkeley.edu': 3,
# 'cwen@iupui.edu': 5, 'antranig@caret.cam.ac.uk': 1,
# 'rjlowe@iupui.edu': 2, 'gsilver@umich.edu': 3,
# 'david.horwitz@uct.ac.za': 4, 'wagnermr@iupui.edu': 1,
# 'zqian@umich.edu': 4, 'stephen.marquard@uct.ac.za': 2,
# 'ray@media.berkeley.edu': 1}
# fd = open('code3/mbox-short.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     if len(words) < 2 or words[0] != 'From':
#         continue
#     email = words[1]
#     res_dict[email] = res_dict.get(email, 0) + 1
# print(res_dict)

# 练习 4： 将代码添加到上述程序中，以确定谁在文件中拥有最多的消息。
# 读取所有数据并创建字典后，使用 maximum 循环（请参阅第 5 章：最大和最小循环）查看字典，
# 以查找谁拥有最多的消息并打印该人拥有多少消息。

# Enter a file name: mbox-short.txt
# cwen@iupui.edu 5

# Enter a file name: mbox.txt
# zqian@umich.edu 195
# fd = open('code3/mbox.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     if len(words) < 2 or words[0] != 'From':
#         continue
#     email = words[1]
#     res_dict[email] = res_dict.get(email, 0) + 1

# v_max = None
# k_max = None
# for k,v in res_dict.items():
#     if v_max == None or v > v_max:
#         v_max, k_max = v, k
# if v_max != None:
#     print(k_max, v_max)


# 练习 5： 该程序记录邮件发送的域名（而不是地址），而不是邮件的来源（即整个电子邮件地址）。在程序结束时，打印出词典的内容。

# 示例行：

# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008

# python schoolcount.py
# Enter a file name: mbox-short.txt
# {'media.berkeley.edu': 4, 'uct.ac.za': 6, 'umich.edu': 7,
# 'gmail.com': 1, 'caret.cam.ac.uk': 1, 'iupui.edu': 8}
# fd = open('code3/mbox-short.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     if len(words) < 2 or words[0] != 'From':
#         continue
#     domain = words[1].split('@')[1]
#     res_dict[domain] = res_dict.get(domain, 0) + 1
# print(res_dict)