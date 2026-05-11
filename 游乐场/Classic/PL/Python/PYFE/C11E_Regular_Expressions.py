import re
# 练习 1： 编写一个简单的程序来模拟 Unix 上的 grep 命令的运行。
# 要求用户输入一个正则表达式，并计算匹配该正则表达式的行数：

# $ python grep.py
# Enter a regular expression: ^Author
# mbox.txt had 1798 lines that matched ^Author

# $ python grep.py
# Enter a regular expression: ^X-
# mbox.txt had 14368 lines that matched ^X-

# $ python grep.py
# Enter a regular expression: java$
# mbox.txt had 4175 lines that matched java$

# # re_exp = input('Enter a regular expression: ')
# re_exps = ['^Author', '^X-', 'java$']
# def grep(re_exp):
#     fd = open('code3/mbox.txt')
#     count = 0
#     for line in fd:
#         if re.search(r''+re_exp, line):
#             count += 1
#     fd.close()
#     print(f'mbox.txt had {count} lines that matched {re_exp}')
# for e in re_exps:
#     grep(e)

# 练习 2： 编写一个程序查找如下格式的行：

# New Revision: 39772
# 使用正则表达式和 findall() 方法从每行中提取数字。
# 计算这些数字的平均值，并以整数形式打印出平均值。

# Enter file:mbox.txt
# 38549

# Enter file:mbox-short.txt
# 39756

# def e2(file_name):
#     fd = open(file_name)
#     total_sum = 0
#     total_count = 0

#     for line in fd:
#         digit_list = re.findall('^New Revision: ([0-9]+)', line)
#         for num in digit_list:
#             total_sum += int(num)
#         total_count += len(digit_list)
#     print(total_sum//total_count)
            
# file_names = ['mbox.txt', 'mbox-short.txt']
# for file_name in file_names:
#     e2('code3/'+file_name)

