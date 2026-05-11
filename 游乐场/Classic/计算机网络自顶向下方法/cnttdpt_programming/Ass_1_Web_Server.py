#import socket module
from socket import *
import threading
import sys # In order to terminate the program

# 对客户端连接的多线程处理函数
def client_handler(connect_socker, print_count):
    try:
        #Fill in start
        message = connect_socker.recv(1024).decode()    
        if print_count > 0: 
            print(repr(message))   
        #Fill in end

        filename = message.split()[1]
        f = open(filename[1:])
        #Fill in start
        outputdata = f.read()
        #Fill in end

        #Send one HTTP header line into socket
        #Fill in start
        resp_head = 'HTTP/1.0 200 OK\r\n' +\
            'Content-Type: text/html; charset=UTF-8\r\n' +\
            f'Content-Length: {len(outputdata)}\r\n' +\
            'Connection: close\r\n' +\
            '\r\n'
        if print_count > 0: 
            print(repr(resp_head)) # 查看包含空白字符的字符串
        connect_socker.send(resp_head.encode())
        #Fill in end

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connect_socker.send(outputdata[i].encode())
        
        connect_socker.close()
    except IOError:
        #Send response message for file not found
        #Fill in start
        resp_body = '404 Not Found'
        resp_head = 'HTTP/1.0 404 Not Found\r\n' +\
            'Content-Type: text/html; charset=UTF-8\r\n' +\
            f'Content-Length: {len(resp_body)}\r\n' +\
            '\r\n'
        connect_socker.send(resp_head.encode())
        connect_socker.send(resp_body.encode())
        #Fill in end

        #Close client socket
        #Fill in start
        connect_socker.close()
        #Fill in end

'''
http://127.0.0.1:1248/test.html
'''

server_socket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 设置套接字的 通用选项-端口复用-开启
server_port = 1248
server_socket.bind(('', server_port))
server_socket.listen()
#Fill in end

print_count = 3 # 打印调试内容次数
while True:
    #Establish the connection
    print('Ready to serve...')
    #Fill in start
    connect_socker, addr = server_socket.accept()
    #Fill in end

    # 设置多线程
    print_count -= 1
    thread = threading.Thread(target=client_handler, args=(connect_socker, print_count))
    thread.daemon = True  # 设为守护线程，主程序退出时自动终止[4][7]
    thread.start()
    


server_socket.close()
sys.exit()#Terminate the program after sending the corresponding data

