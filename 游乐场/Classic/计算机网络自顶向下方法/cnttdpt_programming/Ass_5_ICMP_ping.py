# 发送信息 1秒后超时
from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
# 已给出的校验和
# def checksum(string):
#     csum = 0
#     countTo = (len(string) // 2) * 2
#     count = 0
#     while count < countTo:
#         thisVal = ord(string[count+1]) * 256 + ord(string[count])
#         csum = csum + thisVal
#         csum = csum & 0xffffffff
#         count = count + 2
#     if countTo < len(string):
#         csum = csum + ord(string[len(string) - 1])
#         csum = csum & 0xffffffff
#     csum = (csum >> 16) + (csum & 0xffff)
#     csum = csum + (csum >> 16)
#     answer = ~csum
#     answer = answer & 0xffff
#     answer = answer >> 8 | (answer << 8 & 0xff00)
#     return answer
# @@@提供的checksum有误, 修改后:
def checksum(data):
    """计算ICMP校验和，输入为bytes对象"""
    csum = 0
    count = 0
    length = len(data)
    while count < length - 1:
        this_val = (data[count + 1] << 8) + data[count] # 每次两个字节构建大端序列     
        csum += this_val # 累加
        csum &= 0xffffffff  # 限制为32位
        count += 2 # 步长为2个字节
    # 处理奇数长度
    if count < length:
        csum += data[count]
        csum &= 0xffffffff
    # 折叠进位
    csum = (csum >> 16) + (csum & 0xffff)   # 第一次高/低16位相加
    csum += csum >> 16                      # 第二次处理可能的溢出
    answer = ~csum & 0xffff                 # 取反得到最终校验和
    # 主机序转网络序
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# 接收 ICMP_ECHO_REPLY 结构
# SOCK_RAW 同时捕获ICMP请求包
def receiveOnePing(mySocket, ID, timeout, destAddr):
    print(f'==into receiveOnePing==')
    timeLeft = timeout
    while True:
        startedSelect = time.time()
        # I/O多路复用，等待套接字mySocket在时间timeLeft内接收数据
        whatReady = select.select([mySocket], [], [], timeLeft)
        # 此时为超时或状态改变
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        #Fill in start
        #Fetch the ICMP header from the IP packet
        # 从IP数据包中获取ICMP头部
        # 使用 struct.unpack 进行解包，返回元组
        #@ 得到的包为 IP报头的20字节+ICMP报头+ICMP数据
        first_byte = recPacket[0]
        ip_header_length = (first_byte & 0x0F) * 4  #@ 计算IP头长度，数字*4字节为长度
        print(f'len(recPacket) = {len(recPacket)}, addr = {addr}')
        recv_head = struct.unpack("bbHHh", recPacket[ip_header_length : ip_header_length + 8]) 
        print(f'recv_head = {recv_head}')
        if recv_head[3] != ID or recv_head[0] != 0:
            print(f'--receiveOnePing skip--')
            if recv_head[0] == 3:
                if recv_head[1] == 0:
                    print('Destination Network Unreachable')
                elif recv_head[1] == 1:
                    print('Destination Host Unreachable')
            continue 
        recv_data = struct.unpack("d", recPacket[ip_header_length + 8:ip_header_length + 16]) 
        print(f'recv_data = {recv_data}')
        return timeReceived - recv_data[0]
        #Fill in end
        timeLeft = timeLeft - howLongInSelect
        print(f'timeLeft = {timeLeft}')
        if timeLeft <= 0:
            print(f'==into timeLeft <= 0==')
            return "Request timed out."
        
def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    # 创建一个带有0校验和的虚拟头
    # struct -- 将字符串解释为打包的二进制数据
    # "bbHHh":
    # b	char	整数	1字节
    # H	unsigned short	整数	2字节
    # h	short	整数	2字节
    # d double  浮点数   8
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    print(f'sentdata = {struct.unpack('d', data)}, ID = {ID}')
    # Calculate the checksum on the data and the dummy header.
    # 计算数据和虚拟头的校验和。

    # myChecksum = checksum(str(header + data))
    #@ 修改后的checksum 使用byte类型
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    # 获取正确的校验和，并将其放入标头中
    # Convert 16-bit integers from host to network byte order
    # 将16位整数从主机字节顺序转换为网络字节顺序
    if sys.platform == 'darwin':
        # macOS 特有处理
        myChecksum = htons(myChecksum) & 0xffff  
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    print(f'len(sentPacket) = {len(packet)}')
    mySocket.sendto(packet, (destAddr, 0)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.
    # 列表和元组都由多个对象组成
    # 这些对象可以通过它们在对象中的位置编号来引用。

def doOnePing(destAddr, timeout):
    # getprotobyname("icmp") 获取 ICMP协议 对应协议号
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details:  http://sock-raw.org/papers/sock_raw
    # 创建ICMP套接字
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    # 得到本进程ID
    myID = os.getpid() & 0xFFFF
    # Return the current process i
    # 调用sendOnePing 传入ICMP套接字、目的地址、本进程ID
    sendOnePing(mySocket, destAddr, myID)
    # 调用receiveOnePing 计算延迟
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    # timeout=1 表示：如果一秒钟内没有收到服务器的回复，
    # 客户端会认为客户端的 ping 或服务器的 pong 丢失了。
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    # 向服务器发送大约间隔一秒钟的ping请求
    while 1 :
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)# one second
    return delay

# destAddr = '127.0.0.1'
destAddr = '223.5.5.5'
# destAddr = '192.168.23.23'
timeout_num = 1
test_times = 3
delay_list = []
for i in range(test_times):
    delay_list.append(doOnePing(destAddr, timeout_num))
final_list = [x for x in delay_list if type(x) == float]
lost_rate = (test_times - len(final_list)) / test_times * 100
if lost_rate == 100:
    delay_min, delay_max, delay_avg = 'None', 'None', 'None'
else:
    delay_min = min(final_list)
    delay_max = max(final_list)
    delay_avg = sum(final_list)/test_times
print(f'destAddr = {destAddr}, test_times = {test_times}\nmin = {delay_min}\nmax = {delay_max}\
\navg = {delay_avg}\nlost_rate = {lost_rate}%')