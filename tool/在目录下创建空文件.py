import os
import re

# 设置已存在的输出目录（不动态构造目录）下的完整文件名字符串，若非完整文件名需额外构造
file_str = """
1.o 你的第一个程序 Your First Program.md
2.o 计算机内存 Computer Memory.md
3.o 栈 The Stack.md
4.o 细嚼数字 Nibbling on Numbers.md
5.o 软件内省 Software Introspection.md
6.o 输出与输入 Output and Input.md
7.o 控制流 Control Flow.md
8.o 字节序奇遇 Endian Escapades.md
9.o 汇编杂集 Assembly Assortment.md
10.o 再探栈 The Stack, Revisited.md
11.o 数字即字符串 Numbers as Strings.md
12.o 调试复习 Debugging Refresher.md
13.o 构建 Web 服务器 Building a Web Server.md
"""

# 设置目录路径到原始字符串，
dir_path_str = r'游乐场\o. pwn.college\1.3 Computing 101'

# 通常输入已为完整文件名，若构造文件名，每次任务设置独特格式
def file_name_builder(file_list):
    # 使用 `{中文} {英文}` 字符串构造完成文件名
    # 预期输出添加递增索引与 `.md` 后缀，或使用 LLM 输出完整文件名
    # f"{index}.o {中文} {英文}.md"
    # `1.o 你好，黑客 Hello Hackers.md`

    file_list = [
        rf"{index+1}.o {file_str.strip()}.md" 
        for index, file_str in enumerate(file_list) 
        if file_str
        ]
    return file_list

def dir_file_builder(file_list, dir_path_str):
    """
    输入：
    - file_str
        使用空行分隔的完整文件名字符串
    - dir_path_str
        目录字符串
    """

    # 使用双平台路径分隔符提取路径到列表，之后使用路径合并函数到当前平台格式
    dir_path_list = re.split(r'\\|/', dir_path_str)

    try:
        # 遍历文件列表，在目录下创建文件，使用独占模式确保不覆盖
        for file_name in file_list:
            # 扩展目录路径列表
            file_path = os.path.join(*dir_path_list, file_name)

            print(file_path)
            with open(file_path, 'x') as f:
                pass

    except FileExistsError:
        raise ValueError("目录字符串中的文件已存在")


file_list = file_str.split('\n')
# file_list = get_file_list(file_str) # 若构造完整文件名
file_list = [e.strip() for e in file_list if e] # 若输入完整文件名，直接使用

dir_file_builder(file_list, dir_path_str)