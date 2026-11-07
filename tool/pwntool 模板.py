from pwn import *
from dataclasses import dataclass

# 设置架构
context.arch = "amd64"

# 日志的详细输出使用 debug，仅错误使用 error
# context.log_level = "debug"
# context.log_level = "error"

def connect_process(path="/challenge/run"):
    """
    进程连接包装器，帮助库型函数
    """
    process_tube = process([path])
    return process_tube


def regex_grep_data(re_pattern, origin_data, mod="tuple", index=-1):
    """
    正则表达式提取示例，帮助库型函数
    - 默认返回按位置匹配的元组列表中的最后一个(-1)
    - mod
        - tuple: 返回元组，主调函数按照位置解包
        - dict: 返回字典，主调函数使用 key 引用或设置到类字段
    - index
        - 数字：返回列表索引，默认最后一项
        - None: 返回整个列表
    """
    try:
        match mod:
            case "tuple":
                regex_list = re.findall(re_pattern, origin_data)
                log.debug(f"tuple {regex_list!r}")

            case "dict":
                regex_iter = re.finditer(re_pattern, origin_data)
                regex_list = [regex_match.groupdict() for regex_match in regex_iter]
                log.debug(f"dict {regex_list!r}")

        grep_data = regex_list
        if index != None:
            grep_data = regex_list[index]
            log.debug(grep_data)
    except:
        raise RuntimeError(f"origin_data {origin_data!r}")
    
    return grep_data

@dataclass
class Question_obj:
    sub_lv: int
    obj_lv: int
    subj_cate: set
    obj_cate: set
    action: str

def read_question(cur_tube, levels_list):
    """
    Q 1. Can a Subject with level TS and categories {NATO, NUC, ACE} write an Object with level TS and categories {NUC, ACE}?
    """
    print(">>> into read_question")

    # 读取问题，并提取。使用 recvrepeat 确保特异格式时打印
    question_str = cur_tube.recvrepeat(timeout=0.001)

    level_re_pattern = re.compile(rb'Subject with level (?P<subj_lv>\w+) and categories {(?P<subj_cate>.*)} (?P<action>\w+) an Object with level (?P<obj_lv>\w+) and categories {(?P<obj_cate>.*)}\?')
    level_dict = regex_grep_data(level_re_pattern, question_str, mod="dict")
    print(level_dict)
    
    # 使用列表索引作为先后排序
    sub_lv = levels_list.index(level_dict["subj_lv"])
    obj_lv = levels_list.index(level_dict["obj_lv"])

    question_dict = Question_obj(
        sub_lv=sub_lv,
        obj_lv=obj_lv,
        subj_cate=set(level_dict["subj_cate"].split(b', ') if level_dict["subj_cate"]!=b'' else []),
        obj_cate=set(level_dict["obj_cate"].split(b', ') if level_dict["obj_cate"]!=b'' else []),
        action=level_dict["action"]
    )

    return question_dict

def send_answer(cur_tube, q: Question_obj):
    # 按照列表序，比较主客体设置答案。索引0最低
    print(f">>> into send_answer \nQuestion_obj {q!r}")

    answer = b"no"
    if q.action == b"write":
        # 写入时，从低级到高级，从子集到超集
        ## 等级：主体 <= 客体
        ## 属性：主体 <= 客体
        if q.sub_lv <= q.obj_lv and q.subj_cate <= q.obj_cate:
            answer = b"yes"

    if q.action == b"read":
        # 读取时
        ## 等级：主体 >= 客体
        ## 属性：主体 >= 客体
        if q.sub_lv >= q.obj_lv and q.subj_cate >= q.obj_cate:
            answer = b"yes"

    print(answer)
    cur_tube.sendline(answer)
    res = cur_tube.recvline().strip()
    print(res)
    return res

def task_main(cur_tube):   
    """
    调度主函数，概念型函数
    """
    # 列表数量分界字符串
    levels_delim = b"""Mandatory Access Control (MAC) system:
"""

    cur_tube.recvuntil(levels_delim)
    
    # 之后为列表
    def read_list():
        """
        读取行数后连续读取多行，概念型函数
        预期格式
        4 Levels (first is highest aka more sensitive):
        ...4行...
        或
        4 Categories:
        ...
        """
        # 读取列表元素数量行
        ele_num_str = cur_tube.readline()
        print(f"ele_num_str {ele_num_str!r}")

        # 提取列表元素数量，之后作为列表元素的连续读取次数
        ele_num = int(ele_num_str.split()[0])
        print(f"ele_num {ele_num}")

        # 连续读取行，并清理后构造为列表
        cur_list = [e.strip() for e in cur_tube.recvlines(ele_num)][::-1]
        print(f"cur_list {cur_list!r}")
        return cur_list

    # 读取到 Levels 与 Categories 列表
    levels_list = read_list()
    cate_list = read_list()

    while True:
        question_dict = read_question(cur_tube, levels_list)
        res = send_answer(cur_tube, question_dict)
        if res != b'Correct!':
            raise ValueError("faile")

    cur_tube.interactive()
    cur_tube.close()

cur_tube = connect_process("/challenge/run")
task_main(cur_tube)
