from socket import *
import time

server_name = '127.0.0.1'
server_port = 2345

client_socket = socket(AF_INET, SOCK_DGRAM)
# 使用 settimeout() 设置超时，超时则抛出异常
client_socket.settimeout(1.0)

send_num = 10
rtt_list = []
for i in range(1, send_num+1):
    start_time = time.time()
    client_socket.sendto(f'Ping {i} {start_time}'.encode(),(server_name,server_port))

    try:
        message_get, server_addr = client_socket.recvfrom(2048)
        end_time = time.time()
        print(message_get.decode())
        rtt = (end_time - start_time)
        print(f'rtt: {rtt}')
        rtt_list.append(rtt)
        print('')
    except:
        print('Request timed out')
    
rtt_num = len(rtt_list)
print(f'\nRTT:\nmin: {min(rtt_list)}\nmax: {max(rtt_list)}\navg: {sum(rtt_list)/rtt_num if rtt_num else 0}')
print(f'lost per: {(send_num - rtt_num) / send_num * 100}%')

client_socket.close()