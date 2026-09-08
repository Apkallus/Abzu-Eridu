# Author: https://github.com/abiwaddell
# Throttle the run per-request, and per X requests.
# Full description at https://github.com/abiwaddell/Run-Pause-Resume
import time

# 设置参数
# 每组尝试次数
triedWords=3 
# 每组尝试间隔，分/秒
timeMins=1
timeSecs=2
# 每个请求间隔
throttleMillisecs=5 
# 字典路径
word_list_path = 'E:/auth-lab-passwords.txt'

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           pipeline=False,
                           engine=Engine.BURP
                           )

    # 将每组间隔统一单位到秒
    totalSecs=timeMins*60+timeSecs
    # 循环遍历字典列表
    n=0
    for word in open(word_list_path):
        # 每个请求间隔
        time.sleep(throttleMillisecs/1000)
        engine.queue(target.req, word.rstrip())
        n+=1
        # 每组尝试间隔
        if(n==triedWords):
            time.sleep(totalSecs)
            n=0

def handleResponse(req, interesting):
    if interesting:
        table.add(req)