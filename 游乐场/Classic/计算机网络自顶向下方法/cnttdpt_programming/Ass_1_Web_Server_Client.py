'''
服务器
python Ass_1_Web_Server_Client.py 127.0.0.1 1248 test.html

代理服务器
python Ass_1_Web_Server_Client.py 127.0.0.1 1777 test.html
'''
from socket import *
import sys

# 使用 sys.argv[] 接收命令行参数
# server_name = sys.argv[1]
# server_port = int(sys.argv[2])
# file_name = '/' + sys.argv[3]
server_name = '127.0.0.1'
server_port = 1248
proxy_port = 1777
file_name = '/test.html'

# server_name = '127.0.0.1'
# server_port = 1248

client_socket = socket(AF_INET, SOCK_STREAM)
if proxy_port:
    client_socket.connect((server_name, proxy_port))
else:
    client_socket.connect((server_name, server_port))

head = f'GET {file_name} HTTP/1.1\r\n' +\
    f'Host: {server_name}:{server_port}\r\n' +\
    'Connection: close\r\n' +\
    '\r\n'

client_socket.send(head.encode())

while True:
    message = client_socket.recv(1024).decode()
    if not message:
        break
    print(message)

client_socket.close()