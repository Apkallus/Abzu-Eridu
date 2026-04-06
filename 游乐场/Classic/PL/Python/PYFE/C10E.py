# 练习 1：对之前的程序进行如下修改： 读取并解析“From”行，从该行中提取出地址。
# 使用字典统计每个人发来邮件的数量。

# 在读取完所有数据后，通过从字典中创建一个由（提交次数，电子邮件）元组组成的列表来打印出提交次数最多的人。
# 然后将列表按降序排序，并打印出提交次数最多的人。

# Sample Line:
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008

# Enter a file name: mbox-short.txt
# cwen@iupui.edu 5

# Enter a file name: mbox.txt
# zqian@umich.edu 195

# fd = open('code3/mbox-short.txt')
# res_dict = {}
# for line in fd:
#     words = line.split()
#     if len(words) < 2 or words[0] != 'From':
#         continue
#     email = words[1]
#     res_dict[email] = res_dict.get(email, 0) + 1
# res_dtol = list(res_dict.items())
# res_dtol.sort(key=lambda x: x[1], reverse=True)
# print(res_dtol[0][0], res_dtol[0][1])

# 练习 2：此程序统计一天中每个小时收到的邮件数量。
# 您可以通过查找时间字符串，然后使用冒号字符将该字符串分割成多个部分，从“From”行中提取出小时数。
# 一旦累计了每个小时的数量，就按小时排序，每行打印一个数量，如下所示。

# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008

# python timeofday.py
# Enter a file name: mbox-short.txt
# 04 3
# 06 1
# 07 1
# 09 2
# 10 3
# 11 6
# 14 1
# 15 2
# 16 4
# 17 2
# 18 1
# 19 1
# fd = open('code3/mbox-short.txt')
# hours_dict = {}
# for line in fd:
#     parts = line.split()
#     if len(parts) < 1 or parts[0] != 'From':
#         continue
#     times = parts[5]
#     hours = times.split(':')[0]
#     hours_dict[hours] = hours_dict.get(hours, 0) + 1
# hours_list = list(hours_dict.items())
# hours_list.sort()
# for k,v in hours_list:
#     print(k, v)



# 练习 3：编写一个程序，读取一个文件并打印出按出现频率从高到低排列的字母。

# 您的程序应当将所有输入转换为小写，并且只计算字母 a 到 z。
# 您的程序不应计算空格、数字、标点符号或除字母 a 到 z 之外的任何内容。
# 从几种不同的语言中找到文本样本，看看不同语言中字母出现的频率有何差异。
# 将您的结果与 https://wikipedia.org/wiki/Letter_frequencies 上的表格进行比较。
# import string
# fd = open('code3/mbox-short.txt')
# ch_dict = {}
# for line in fd:
#     ## 去除字母外的字符
#     # words = line.translate(str.maketrans('','',string.punctuation + ' \n\t' + string.digits)).lower()
#     # for ch in words:
#     #     ch_dict[ch] = ch_dict.get(ch, 0) + 1
#     ## 只记录字母字符
#     words = line.lower()
#     for ch in words:
#         if ch in string.ascii_lowercase:
#             ch_dict[ch] = ch_dict.get(ch, 0) + 1

# ch_list = list(ch_dict.items())
# ch_list.sort(key=lambda x:x[1], reverse=True)
# for k,v in ch_list:
#     print(k, v)