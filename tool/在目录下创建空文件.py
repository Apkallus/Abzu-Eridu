import os
import re

# 设置输出目录下的完整文件名字符串，若非完整文件名需额外构造
file_str = """
1.o 你好，黑客 Hello Hackers.md
2.o 探究路径 Pondering Paths.md
3.o 理解命令 Comprehending Commands.md
4.o 消化文档 Digesting Documentation.md
5.o 文件通配 File Globbing.md
6.o 练习管道 Practicing Piping.md
7.o Shell 变量 Shell Variables.md
8.o 数据操作 Data Manipulation.md
9.o 进程与作业 Processes and Jobs.md
10.o 理清用户 Untangling Users.md
11.o 认识权限 Perceiving Permissions.md
12.o 串联命令 Chaining Commands.md
13.o 终端复用 Terminal Multiplexing.md
14.o 探究 PATH Pondering PATH.md
15.o 滑稽把戏 Silly Shenanigans.md
16.o 大胆破坏 Daring Destruction.md
17.o 进阶学习 Further Learning.md
"""

# 设置目录路径到原始字符串，
dir_path_str = r'游乐场\pwn.college\1.1 Linux Luminarium'

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