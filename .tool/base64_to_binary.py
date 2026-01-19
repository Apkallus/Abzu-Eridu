import base64
from mylib import *

# 复制 Base64 编码的二进制文件到 tmp_file_name 文件后执行程序解码

tmp_file_name = ".\\.tool\\base64_to_binary_file"

base64_data = read_or_creat_file(tmp_file_name)

print(len(base64_data))

binary_data = base64.b64decode(base64_data)

print(len(binary_data))

write_to_file(tmp_file_name, binary_data, "wb")
