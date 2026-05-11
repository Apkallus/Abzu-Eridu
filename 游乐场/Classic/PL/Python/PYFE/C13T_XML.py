# 从 XML 中提取数据

# 在这个作业中，你将编写一个与 http://www.py4e.com/code3/xml3.py 程序将提示输入一个 URL，
# 然后使用该 URL 读取 XML 数据 urllib，然后解析并从 XML 数据中提取评论计数，计算文件中所有数字的总和。

# 我们为这个作业提供了两个文件。一个是示例文件，我们为你提供了用于测试的数字总和；
# 另一个是你要为作业处理的真实数据文件。

# 示例数据：http://py4e-data.dr-chuck.net/comments_42.xml （和=2553）
# 实际数据：http://py4e-data.dr-chuck.net/comments_2252169.xml (和为16)
# 你不需要将这些文件保存到你的文件夹中，因为你的 程序将直接从 URL 读取数据。 
# 注意： 每位学生都会有一个独特的作业数据 URL——因此，请只使用您自己的 自己的数据 URL 用于分析。
# 数据格式和方法
# 数据由多个名称和评论计数组成，XML 格式如下：

# <comment>
#   <name>Matthias</name>
#   <count>97</count>
# </comment>
# 你需要查看所有的 标签并找到 值 将数字相加。 最接近的示例代码，展示如何解析 XML 的是 xml3.py
# 为了简化代码，您可以使用 XPath 选择器字符串来遍历整个 XML 树，查找任何名为'count'的标签，代码如下：

# counts = tree.findall('.//count')
# 查看 Python ElementTree 文档，并查找支持的 XPath 语法以获取详细信息。
# 你也可以从 XML 的顶部向下到评论节点，然后遍历评论节点的子节点。
# 示例执行


# $ python3 solution.py
# Enter location: http://py4e-data.dr-chuck.net/comments_42.xml
# Retrieving http://py4e-data.dr-chuck.net/comments_42.xml
# Retrieved 4189 characters
# Count: 50
# Sum: 2...

from urllib.request import urlopen
import  xml.etree.ElementTree as ET

# url = 'http://py4e-data.dr-chuck.net/comments_42.xml'
url = 'http://py4e-data.dr-chuck.net/comments_2252169.xml'
urld = urlopen(url)
data = urld.read()
xtree = ET.fromstring(data)

counts_list = xtree.findall('.//count')
count_sum = 0
count_num = 0
for count_e in counts_list:
    count_sum += int(count_e.text)
    count_num += 1

print('Count:', count_num)
print('Sum:', count_sum)