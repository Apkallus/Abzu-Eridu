# 探索超文本传输协议

# 您需要使用 HTTP 协议获取以下文档，以便检查 HTTP 响应头。

# http://data.pr4e.org/intro-short.txt
# 有三种方法可以获取此网页并查看响应头：

# 首选： 修改 socket1.py 程序用于获取上述 URL 并打印出头部和数据。 
# 确保将代码更改为获取上述 URL——每个 URL 的值都不同。
# 在带有开发者控制台或 FireBug 的网页浏览器中打开 URL，并手动检查返回的头部。

import urllib.request, urllib.parse, urllib.error
usr_url = 'http://data.pr4e.org/intro-short.txt'
fd = urllib.request.urlopen(usr_url)
# 使用.headers直接得到head
print(fd.headers)