# 设置目录字符串
file_str = """
格式化字符串漏洞利用 Format String Exploits  
文件结构漏洞利用 File Struct Exploits  
利用原语 Exploitation Primitives  
动态分配器利用 Dynamic Allocator Exploitation  
内核利用 Kernel Exploitation
"""
# 将目录字符串拆分为字符串列表，遍历列表创建对应文件

# 设置目录路径
filepath = '游乐场\\pwn.college\\2.4 Software Exploitation'

file_list = file_str.split('\n')
# 去掉前后空白符号
file_clear_list = [e.strip() for e in file_list if e]
print(file_clear_list)

try:
    for index, new_file in enumerate(file_clear_list):
        with open(f'{filepath}\\{str(index+1)}. {new_file}.md', 'x', encoding='utf-8') as f:
            pass
except FileExistsError:
    print('目录字符串中的文件已存在')
    raise

