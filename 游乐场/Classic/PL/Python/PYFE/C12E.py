# 练习 1： 修改套接字程序 socket1.py 以提示用户输入 URL，使其能够读取任何网页。

# 你可以使用 split('/') 将 URL 分割成其 组成部分，以便提取用于套接字的域名 connect 调用。
# 使用 try 添加错误检查。 except 来处理用户输入格式不正确或 URL 不存在的情况。

# import socket
# # ipv4 tcp
# mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# usr_url = input('url: ')
# try:
#       # 0->'http:', 1->'', 2->'data.pr4e.org', 3->'romeo.txt'
#     usr_domine = usr_url.split('/')[2]
#     # mysock.connect(('data.pr4e.org', 80))
#     mysock.connect((usr_domine, 80))
#       # python使用unicode编码，http使用utf-8编码，于是使用encode()与decode()进行格式转换
#     # cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
#     cmd = f'GET {usr_url} HTTP/1.0\r\n\r\n'.encode()
#     mysock.send(cmd)
# except:
#     print('error: improperly formatted or non-existent URL')
#     exit()

# while True:
#     data = mysock.recv(512)
#     if len(data) < 1:
#         break
#     print(data.decode(),end='')

# mysock.close()

# 练习 2： 修改你的套接字程序，使其计算接收到的字符数，并在显示 3000 个字符后停止显示任何文本。
# 该程序应检索整个文档并计算总字符数，在文档末尾显示字符计数。

# import socket
# # ipv4 tcp
# mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # usr_url = input('url: ')
# usr_url = 'http://data.pr4e.org/romeo-full.txt'
# try:
#     usr_domine = usr_url.split('/')[2]
#     # mysock.connect(('data.pr4e.org', 80))
#     mysock.connect((usr_domine, 80))
#     # cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
#     cmd = f'GET {usr_url} HTTP/1.0\r\n\r\n'.encode()
#     mysock.send(cmd)
# except:
#     print('error: improperly formatted or non-existent URL')
#     exit()

## 使用变量累计字节数量，is_out为是否超过的flag变量
# count_len = 0
# is_out = False
# # output = 0
# while True:
#     data = mysock.recv(512)
#     data_len = len(data)
#     if data_len < 1:
#         break
#     count_len += data_len
#       # 如果没有超过限制则直接发送
#     if count_len <= 3000:
#         print(data.decode(),end='')
#         # output += data_len
#         if count_len == 3000:
#             is_out = True
#       # 如果在本次接受后才超过，即flag变量为false
#       # 3000 - count_len得到超过的负index, [:此index]即为在范围内的字符切片
#       # 输出未超过部分的字符，并更新flag变量
#     elif is_out == False:      
#         print(data[:3000 - count_len].decode(),end='')
#         # output += len(data[:3000 - count_len])
#         # print('\n',count_len, output, len(data[:3000 - count_len]))
#         is_out = True
# print(count_len)

# mysock.close()

# 练习 3： 使用 urllib 来复制之前的练习，即 (1) 从 URL 获取文档，(2) 显示最多 3000 个字符，
# 以及 (3) 计算文档中字符的总数。这次练习不用担心头部信息，只需显示文档内容的前 3000 个字符。
# import urllib.request, urllib.parse, urllib.error
# usr_url = 'http://data.pr4e.org/romeo-full.txt'
# fd = urllib.request.urlopen(usr_url)
# 直接读取即为不包含头部的body
# print(fd.read(3000).decode())


# 练习 4： 修改 urllinks.py 程序用于提取和统计检索到的 HTML 中的段落（p）标签 记录并显示段落数量作为输出 程序。
# 不要显示段落文本，只计算它们。测试你的 在多个小网页以及一些较大的网页上运行程序。
# import urllib.request, urllib.parse, urllib.error
# from bs4 import BeautifulSoup
# import ssl # defauts to certicate verification and most secure protocol (now TLS)

# # Ignore SSL/TLS certificate errors
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

# # url = input('Enter - ')
# url = 'https://docs.python.org'
# html = urllib.request.urlopen(url, context=ctx).read()
# soup = BeautifulSoup(html, 'html.parser')

# ps = soup('p')
# print(len(ps))

# 练习 5: (高级) 修改套接字程序，使其仅在接收到头部和空行后显示数据。
# 请记住，recv 接收的是字符（包括换行符），而不是行。


# import socket
# # ipv4 tcp
# mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # usr_url = input('url: ')
# usr_url = 'http://data.pr4e.org/romeo-full.txt'
# try:
#     usr_domine = usr_url.split('/')[2]
#     # mysock.connect(('data.pr4e.org', 80))
#     mysock.connect((usr_domine, 80))
#     # cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
#     cmd = f'GET {usr_url} HTTP/1.0\r\n\r\n'.encode()
#     mysock.send(cmd)
# except:
#     print('error: improperly formatted or non-existent URL')
#     exit()

## 累计头部信息，直到找到空行，并输出剩余body
# head = b''
# count_len = 0
# is_out = False
# while True:
#     data = mysock.recv(512)
#     head += data
#     end_of_head = head.find(b'\r\n\r\n')
#     if end_of_head != -1:
#           # 空行的正index - len得到负index
#         head_neg_index = end_of_head - len(head)
#           # 负index与正index都为左小右大，+4得到body部分的index
#         body_index = head_neg_index+4
#         body = data[body_index:]
#         print(body.decode())
#         count_len += len(body)
#         break
#     data_len = len(data)
#     if data_len < 1:
#         exit()

## body部分输出直到字符数量限制
# while True:
#     data = mysock.recv(512)
#     data_len = len(data)
#     if data_len < 1:
#         break
#     count_len += data_len
#     if count_len <= 3000:
#         print(data.decode(),end='')
#         if count_len == 3000:
#             is_out = True
#     elif is_out == False:      
#         print(data[:3000 - count_len].decode(),end='')
#         is_out = True

# print()
# mysock.close()