# 在干草堆中找数字

# 在这个作业中，你将读取并解析一个包含文本和数字的文件。你需要提取文件中的所有数字，并计算这些数字的总和。

# 数据文件
# 我们为这个作业提供了两个文件。一个是示例文件，我们为你提供了用于测试的数字总和；另一个是你要为作业处理的真实数据文件。

# 样本数据：http://py4e-data.dr-chuck.net/regex_sum_42.txt （有90个值，和为445833）
# 实际数据：http://py4e-data.dr-chuck.net/regex_sum_2252165.txt （有63个值，和以652结尾）
# 这些链接将在新窗口中打开。 确保将文件保存在你将要编写 Python 程序的同一文件夹中。 
# 注意： 每位学生都将有一个独特的作业数据文件——因此，请只使用您的 自己的数据文件用于分析。
# 数据格式
# 该文件包含教科书引言中的大部分文本，只是在整个文本中插入了随机数。以下是您可能看到的输出样本：

# Why should you learn to write programs? 7746
# 12 1929 8827
# Writing programs (or programming) is a very creative 
# 7 and rewarding activity.  You can write programs for 
# many reasons, ranging from making your living to solving
# 8837 a difficult data analysis problem to having fun to helping 128
# someone else solve a problem.  This book assumes that 
# everyone needs to know how to program ...

# 上述样本文本的总和是 27486。 数字可以出现在行的任何位置。每行可以有任意数量的 数字（包括没有）。
# 处理数据
# 这个问题的基本框架是读取文件，使用 re.findall()，查找正则表达式 '[0-9]+'，然后将提取的字符串转换为整数并求和。
import re

def e2(file_name):
    fd = open(file_name)
    total_sum = 0
    total_count = 0

    for line in fd:
        digit_list = re.findall('[0-9]+', line)
        for num in digit_list:
            total_sum += int(num)
        total_count += len(digit_list)
    print(total_count, total_sum)
    fd.close()
            
# file_names = ['regex_sum_42.txt', 'regex_sum_2252165.txt']
# for file_name in file_names:
#     e2(file_name)

## 列表推导式
fd = open('regex_sum_2252165.txt')
print(sum([int(num) for line in fd for num in re.findall('[0-9]+', line)]))