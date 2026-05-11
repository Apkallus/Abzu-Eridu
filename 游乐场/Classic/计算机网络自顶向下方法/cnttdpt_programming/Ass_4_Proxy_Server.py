from socket import *
import threading
import sys

def forword_data(src, dst):
    while True:
        data = src.recv(4096)
        if not data:
            break
        dst.send(data)

# 不存在时向服务器请求文件
def server_request(server_name, server_port, header):
    print('into server_request'.center(40, '=') + '\n')
    print(f'server_name, server_port: {server_name, server_port}\n')
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    client_socket.send(header.encode())

    message = b''
    while True:
        new_message = client_socket.recv(1024)
        if not new_message:
            break
        message += new_message
    client_socket.close()

    # 提取报头与空行
    bland_line_index = message.find(b'\r\n\r\n')
    print(f'bland_line_index: {bland_line_index}\n')
    server_header = message[:bland_line_index + 4:]
    server_body = message[bland_line_index + 4:]
    print(f'server_header.decode: {server_header.decode()}')
    print(f'server_body.decode: {server_body.decode()}')
    print('out server_request'.center(40, '=') + '\n')
    return server_header, server_body
    

# 对客户端连接的多线程处理函数
# 示例为读取缓存在磁盘的文件，实现使用缓存在内存
# cache_dict key为URL, value为文件数据与文件类型， 文件类型从目的服务器得到
# 如之后扩展到磁盘，在检查内存后再检查磁盘清单
def client_handler(connect_socker, print_count, cache_dict):
    print('into client_handler'.center(40, '=') + '\n')
    header = connect_socker.recv(1024).decode()   
    if print_count > 0: 
        print(f'repr(header): {repr(header)}')   

    head_line = header.split('\r\n') # 按行分割为列表
    method = head_line[0].split()[0]
    print(f'method: {method}\n')

    file_name = head_line[0].split()[1]

    for line in head_line:
        if 'Host:' in line:
            # Host: 127.0.0.1:1248\r\n
            host_line = line.split(':')
            server_name = host_line[1][1:]
            server_port = int(host_line[2])
            break
    file_url = server_name + file_name
    print(f'file_url: {file_url}\n')

    if method == 'CONNECT':
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_name, server_port))
        print(f'server_name, server_port: {server_name, server_port}\n')
        threading.Thread(target=forword_data, args=(connect_socker, client_socket)).start()
        threading.Thread(target=forword_data, args=(client_socket, connect_socker)).start()
        # 向客户端发送隧道建立成功的确认信号（200 Connection Established）
        connect_socker.send(b"HTTP/1.1 200 Connection Established\r\n\r\n") 
        return
    elif method != 'GET':
        server_header, server_body = server_request(server_name, server_port, header)
        connect_socker.send(server_header)
        connect_socker.send(server_body)
        connect_socker.close()
        return

    # 查看文件是否缓存在内存中
    if file_url in cache_dict:
        print('in cache_dict'.center(30, '='))
        # 得到文件数据与类型
        file_data, file_type = cache_dict[file_url]

        #Send one HTTP header line into socket
        resp_head = 'HTTP/1.0 200 OK\r\n' +\
            f'Content-Type: {file_type}\r\n' +\
            f'Content-Length: {len(file_data)}\r\n' +\
            'Connection: close\r\n' +\
            '\r\n'
        if print_count > 0: 
            print(repr(resp_head)) # 查看包含空白字符的字符串
        connect_socker.send(resp_head.encode())

        #Send the content of the requested file to the client
        connect_socker.send(file_data)
        connect_socker.close()
    else:
        print('not in cache_dict'.center(30, '=') + '\n')
        # 如不存在于缓存中
        server_header, server_body = server_request(server_name, server_port, header)

        server_header_line = server_header.decode().split('\r\n') # 按行分割为列表
        print(repr(server_header_line))
        for line in server_header_line:
            print(line)
            if 'Content-Type:' in line:
                # Host: 127.0.0.1:1248\r\n
                file_type = line.split(':')[1][1:]
                break

        connect_socker.send(server_header)
        connect_socker.send(server_body)
        connect_socker.close()

        cache_dict[file_url] = (server_body, file_type)


# if len(sys.argv) <= 1:
#     print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#     sys.exit(2)

# Create a server socket, bind it to a port and start listening
server_socket = socket(AF_INET, SOCK_STREAM)
# Fill in start.
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 设置套接字的 通用选项-端口复用-开启
server_port = 1777
server_socket.bind(('', server_port))
server_socket.listen()
# Fill in end.

# 内存中缓存字典为 cache_dict
cache_dict = {}
print_count = 3 # 打印调试内容次数
while True:
    print_count -= 1
    # Strat receiving data from the client
    print('Ready to serve'.center(50, '=') + '\n')
    connect_socker, addr = server_socket.accept()
    print('Received a connection from:', addr)

    # 设置多线程
    thread = threading.Thread(target=client_handler, args=(connect_socker, print_count, cache_dict))
    thread.daemon = True  # 设为守护线程，主程序退出时自动终止[4][7]
    thread.start()

# Fill in start.
server_socket.close()
sys.exit()#Terminate the program after sending the corresponding data
# Fill in end.