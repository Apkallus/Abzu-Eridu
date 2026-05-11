# 在 Python 中跟随链接

# 在这个作业中，你将编写一个 Python 程序，扩展 http://www.py4e.com/code3/urllinks.py。
# 该程序将使用 urllib 读取下方数据文件中的 HTML，从锚标签中提取 href 值，
# 扫描相对于列表中第一个名字处于特定位置的标签，跟随该链接并重复该过程多次，并报告你找到的最后一个名字。

# 我们为这个作业提供了两个文件。一个是示例文件，我们为你提供了名字用于测试；另一个是你要为作业处理的真实数据文件

# 示例问题：从 http://py4e-data.dr-chuck.net/known_by_Fikret.html
# 找到位置 3（第一个名称是 1）的链接。 点击那个链接。重复这个步骤 4 次。 答案是您最后检索到的姓氏。
# 姓名序列：Fikret Montgomery Mhairade Butchi Anayah
# 序列中的最后一个姓氏：Anayah
# 实际问题：从 http://py4e-data.dr-chuck.net/known_by_Cheyenne.html 开始
# 找到位置 18 的链接（第一个名称是 1）。 点击那个链接。重复这个步骤 7 次。 answer 是你最后检索到的姓氏。
# 提示：您将要加载的最后一页的名称的第一个字符是：J
# 策略
# 网页通过调整链接之间的高度并在几秒钟后隐藏页面，以使你不编写 Python 程序就难以完成作业。
# 但坦率地说，只需稍加努力和耐心，你就能克服这些尝试，使不编写 Python 程序完成作业变得稍微困难一些。
# 但这并不是重点。重点是编写一个聪明的 Python 程序来解决这个程序。

# 示例执行

# 以下是一个解决方案的示例执行：

# $ python3 solution.py
# Enter URL: http://py4e-data.dr-chuck.net/known_by_Fikret.html
# Enter count: 4
# Enter position: 3
# Retrieving: http://py4e-data.dr-chuck.net/known_by_Fikret.html
# Retrieving: http://py4e-data.dr-chuck.net/known_by_Montgomery.html
# Retrieving: http://py4e-data.dr-chuck.net/known_by_Mhairade.html
# Retrieving: http://py4e-data.dr-chuck.net/known_by_Butchi.html
# Retrieving: http://py4e-data.dr-chuck.net/known_by_Anayah.html
# 这次执行作业的答案是"Anayah"。

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re

count = 7
position = 18

def check(url, position):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # url = 'http://py4e-data.dr-chuck.net/known_by_Cheyenne.html'
    # url = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'
    html = urlopen(url, context = ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup('a')
    # for tag in tags:
    # # TAG: <a href="http://py4e-data.dr-chuck.net/known_by_Cohen.html">Cohen</a>
    # # Contents: ['Cohen']
    # # Attrs: {'href': 'http://py4e-data.dr-chuck.net/known_by_Cohen.html'}
    # # URL: http://py4e-data.dr-chuck.net/known_by_Cohen.html
    #     print('TAG:', tag)
    #     print('Contents:', tag.contents)
    #     print('Attrs:', tag.attrs)
    #     print('URL:', tag.get('href', None))
    ## 解析后得到标签列表，使用位置-1作为偏移得到对应标签
    tag = tags[position - 1]
    ## 返回标签内数据以字典形式存储，得到href为key的对应url
    return tag.get('href', None), tag.contents

url = 'http://py4e-data.dr-chuck.net/known_by_Cheyenne.html'
# url = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'
for i in range(count):
    # 使用返回的url更新变量，循环调用
    url, name = check(url, position)
    print(url, name)
