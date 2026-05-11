# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 设置套接字的 通用选项-端口复用-开启
serverSocket.bind(('', 2345))

last_recv_no, last_recv_time = None, None
while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    print(rand)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)


    # Capitalize the message from the client
    send_message = message.decode().upper()
    # If rand is less is than 4, we consider the packet lost and do not respond
    # if rand < 4:
    #     continue
    if rand >= 4:
        message_list = message.decode().split()
        if last_recv_no == None:
            last_recv_no = int(message_list[1])
            last_recv_time = float(message_list[2])
        else:
            new_recv_no = int(message_list[1])
            new_recv_time = float(message_list[2])
            
            time_dif = new_recv_time - last_recv_time
            lose_recv_no_list = [str(i) for i in range(last_recv_no + 1, new_recv_no)]
            lose_recv_no_str = f'lost_no: ' + ' ,'.join(lose_recv_no_list)
            print(f'recv_no: {new_recv_no}')
            print(lose_recv_no_list)
            send_message += f'\ntime_dif: {time_dif}'
            if len(lose_recv_no_list):
                send_message += '\n' + lose_recv_no_str
            last_recv_no = new_recv_no
            last_recv_time = new_recv_time
        # Otherwise, the server responds
        serverSocket.sendto(send_message.encode(), address)