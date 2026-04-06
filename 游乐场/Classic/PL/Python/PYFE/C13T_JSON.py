# 在这个作业中，你将编写一个与 http://www.py4e.com/code3/json2.py 程序将提示输入一个 URL，
# 然后使用该 URL 读取 JSON 数据 urllib，然后解析并从 JSON 数据中提取评论计数，计算文件中数字的总和，并将总和输入下方：

# 我们为这个作业提供了两个文件。一个是示例文件，我们为你提供了用于测试的数字总和；
# 另一个是你要为作业处理的真实数据文件。

# 示例数据：http://py4e-data.dr-chuck.net/comments_42.json (Sum=2553)
# 实际数据：http://py4e-data.dr-chuck.net/comments_2252170.json (Sum ends with 22)
# 你不需要将这些文件保存到你的文件夹中，因为你的 程序将直接从 URL 读取数据。 
# 注意： 每位学生都会有一个独特的作业数据 URL——因此，请只使用您自己的 自己的数据 URL 用于分析。
# 数据格式
# 数据包含一些名称和评论计数，以 JSON 格式如下：

# {
#   comments: [
#     {
#       name: "Matthias"
#       count: 97
#     },
#     {
#       name: "Geomer"
#       count: 97
#     }
#     ...
#   ]
# }
# 最接近的示例代码，展示如何解析 JSON 并提取列表的是 json2.py。
# 你可能还想 要查看 xml3.py 来看看如何提示输入 URL 并从 URL 获取数据。

# 示例执行

# $ python3 solution.py
# Enter location: http://py4e-data.dr-chuck.net/comments_42.json
# Retrieving http://py4e-data.dr-chuck.net/comments_42.json
# Retrieved 2733 characters
# Count: 50
# Sum: 2...

# {
#   "note":"This file contains the sample data for testing",
#   "comments":[
#     {
#       "name":"Romina",
#       "count":97
#     },
#     {
#       "name":"Laurie",
#       "count":97
#     },

from urllib.request import urlopen
import json

# url = 'http://py4e-data.dr-chuck.net/comments_42.json'
url = 'http://py4e-data.dr-chuck.net/comments_2252170.json'
data = json.loads(urlopen(url).read().decode())

res_sum = 0
for e in data['comments']:
    print(e)
    res_sum += int(e['count'])
print(res_sum)
