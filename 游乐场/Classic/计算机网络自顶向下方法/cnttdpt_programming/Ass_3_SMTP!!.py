from socket import *

'''
telnet smtp-mail.outlook.com 587 
# 端口 25非加密 或 587加密
'''

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
mailserver_name = 'smtp-mail.outlook.com'
mailserver_port = 587
#Fill in end

# Create socket called client_socket and establish a TCP connection with mailserver
#Fill in start
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((mailserver_name, mailserver_port))
#Fill in end

recv_msg = client_socket.recv_msg(1024).decode()
print(recv_msg)
if recv_msg[:3] != '220':
    print('220 reply not received from server.')

#========加密==========
# 发送 STARTTLS 加密连接
STARTTLS_Command = 'STARTTLS\r\n'
client_socket.send(STARTTLS_Command.encode())
recv_msg1 = client_socket.recv_msg(1024).decode()
print(recv_msg1)
if recv_msg1[:3] != '220':
    print('220 reply not received from server.')

import ssl
#@@ 创建 SSL 上下文 (强制证书验证)
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2  # 设置最低 TLS 版本

#@@ 将原始 Socket 升级为加密 Socket
ssl_sock = context.wrap_socket(
    client_socket, 
    server_hostname = mailserver_name  # 用于证书域名验证
)
print(f"加密协议: {ssl_sock.version()}")
print(f"证书信息: {ssl_sock.getpeercert()}")
#========加密==========
# Send HELO command and print server response.
heloCommand = 'HELO test.com\r\n'
client_socket.send(heloCommand.encode())
recv_msg1 = client_socket.recv_msg(1024).decode()
print(recv_msg1)
if recv_msg1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
mail_from_Command = 'MAIL FROM:<test@test.com>\r\n'
client_socket.send(mail_from_Command.encode())
recv_msg2 = client_socket.recv_msg(1024).decode()
print(recv_msg2)
if recv_msg2[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
rcpt_to_Command = 'RCPT TO:<test@outlook.com>\r\n'
client_socket.send(rcpt_to_Command.encode())
recv_msg3 = client_socket.recv_msg(1024).decode()
print(recv_msg3)
if recv_msg3[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
data_Command = 'DATA\r\n'
client_socket.send(data_Command.encode())
recv_msg4 = client_socket.recv_msg(1024).decode()
print(recv_msg4)
if recv_msg4[:3] != '354':
    print('354 reply not received from server.')
# Fill in end

# Send message data.
# Message ends with a single period.
# Fill in start
message_data = 'From: Sender <test@test.com>\r\n' +\
    'To: Recipient <test@outlook.com>\r\n' +\
    'Subject: Test Email\r\n' +\
    'Content-Type: text/plain; charset=UTF-8\r\n' +\
    '\r\n' +\
    'Hello, this is a test email.\r\n' +\
    '.\r\n'  
client_socket.send(message_data.encode())
recv_msg5 = client_socket.recv_msg(1024).decode()
print(recv_msg5)
if recv_msg5[:3] != '250':
    print('250 reply not received from server.')
# Fill in end

# Send QUIT command and get server response.
# Fill in start
quit_Command = 'QUIT\r\n'
client_socket.send(quit_Command.encode())
recv_msg6 = client_socket.recv_msg(1024).decode()
print(recv_msg6)
if recv_msg6[:3] != '221':
    print('221 reply not received from server.')
# Fill in end
