# 使用 BeautifulSoup 从 HTML 中抓取数字 在这个作业中，
# 你将编写一个类似于 http://www.py4e.com/code3/urllink2.py 的 Python 程序。
# 该程序将使用 urllib 读取下方数据文件中的 HTML，解析数据，提取数字并计算文件中数字的总和。

# 我们为这个作业提供了两个文件。一个是示例文件，我们为你提供了用于测试的数字总和；
# 另一个是你要为作业处理的真实数据文件。

# 示例数据：http://py4e-data.dr-chuck.net/comments_42.html (Sum=2553)
# 实际数据：http://py4e-data.dr-chuck.net/comments_2252167.html (Sum 以 45 结尾)
# 你不需要将这些文件保存到你的文件夹中，因为你的 程序将直接从 URL 读取数据。 
# 注意： 每位学生都会有一个独特的作业数据 URL——因此，请只使用您自己的 自己的数据 URL 用于分析。
# 数据格式
# 该文件是一个包含姓名和评论计数的表格。你可以忽略文件中的大部分数据，只需关注类似以下内容的行：

# <tr><td>Modu</td><td><span class="comments">90</span></td></tr>
# <tr><td>Kenzie</td><td><span class="comments">88</span></td></tr>
# <tr><td>Hubert</td><td><span class="comments">87</span></td></tr>
# 你需要找到文件中所有的<span>标签，并从中提取数字，然后将这些数字相加。
# 看看提供的 示例代码 。它展示了如何查找所有特定类型的标签，遍历这些标签并提取标签的各个部分。

# ...
# # Retrieve all of the anchor tags
# tags = soup('a')
# for tag in tags:
#    # Look at the parts of a tag
#    print 'TAG:',tag
#    print 'URL:',tag.get('href', None)
#    print 'Contents:',tag.contents[0]
#    print 'Attrs:',tag.attrs
# 您需要调整这段代码，以便查找 span 标签并提取 span 标签的文本内容，转换为整数并 将它们加起来完成作业。
# 示例执行


# $ python3 solution.py
# Enter - http://py4e-data.dr-chuck.net/comments_42.html
# Count 50
# Sum 2...

# 如果 import urllib.request, 使用时需写全 urllib.request.urlopen()
# 使用 from urllib.request import urlopen，只需 urlopen()
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url = 'http://py4e-data.dr-chuck.net/comments_42.html'
url = 'http://py4e-data.dr-chuck.net/comments_2252167.html'
html = urlopen(url, context = ctx).read()
soup = BeautifulSoup(html, "html.parser")

# <tr><td>Hubert</td><td><span class="comments">87</span></td></tr>
tags = soup('span')
res_sum = 0
for tag in tags:
# TAG: <span class="comments">2</span>
# Contents: ['2']
# Attrs: {'class': ['comments']}
    # print('TAG:', tag)
    # print('Contents:', tag.contents)
    # print('Attrs:', tag.attrs)
    res_sum += int(tag.contents[0])
print(res_sum)