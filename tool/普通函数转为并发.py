import asyncio
import threading

def 模拟阻塞函数():
    pass

def 并发执行代码的包装函数():
    pass

# 协程型，在协程对象之间调度，直到协程执行完成后继续代码流
## 需包装预期并发执行的后续代码并设置为被调度的协程
async def 协程主函数():
    await asyncio.gather(
        asyncio.to_thread(模拟阻塞函数),
        asyncio.to_thread(并发执行代码的包装函数)
        )

asyncio.run(协程主函数())

# 线程型，将阻塞函数放入子线程，立即返回
## 主线程继续执行，仅需在最后回收子线程
def 线程主函数():
    阻塞函数线程对象 = threading.Thread(target=模拟阻塞函数)

    阻塞函数线程对象.start()
    # 主线程代码继续执行

    阻塞函数线程对象.join()

线程主函数()