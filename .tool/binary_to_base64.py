import base64
from mylib import *

# 复制 Base64 编码的二进制文件到 tmp_file_name 文件后执行程序解码

tmp_file_name = ".cache\\base64_to_binary_file"

file_path = input("file_path")

with open(file_path, 'rb') as f:
    file_data = f.read()

base64_data = base64.b64encode(file_data)

print(len(base64_data))

write_to_file(tmp_file_name, base64_data, "wb")
