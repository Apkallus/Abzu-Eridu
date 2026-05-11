from socket import *

server_port = 12345
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen()

while True:
    connect_socker, addr = server_socket.accept()
    receive_data = connect_socker.recv(1024).decode()
    print(receive_data)
    connect_socker.close()