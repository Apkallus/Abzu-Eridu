# 队列

https://docs.python.org/3/library/asyncio-queue.html

**源代码：** [Lib/asyncio/queues.py](https://github.com/python/cpython/tree/3.15/Lib/asyncio/queues.py)

---

`asyncio` 队列的设计类似于 `[queue]` 模块中的类。尽管 `asyncio` 队列不是线程安全的，但它们专为在 `async`/`await` 代码中使用而设计。

注意，`asyncio` 队列的方法没有 `timeout` 参数；如需执行带超时的队列操作，请使用 `asyncio.wait_for()` 函数。

另请参阅下面的[示例]部分。

## Queue

### class asyncio.Queue()

```py
class asyncio.Queue(maxsize=0)
```

先进先出（FIFO）队列。

如果 `maxsize` 小于或等于零，则队列大小无限。如果它是大于 `0` 的整数，则当队列达到 `maxsize` 时，`await put()` 会阻塞，直到有项被 `get()` 移除。

与标准库 `threading` 的 `[queue]` 不同，队列的大小始终已知，并且可以通过调用 `qsize()` 方法返回。

**3.10 版本变更：** 移除了 `loop` 参数。

此类[非线程安全]。

#### maxsize

队列中允许的项数。

#### empty()

如果队列为空，则返回 `True`，否则返回 `False`。

#### full()

如果队列中有 `maxsize` 个项，则返回 `True`。

如果队列以 `maxsize=0`（默认值）初始化，则 `full()` 从不返回 `True`。

#### async get()

从队列中移除并返回一个项。如果队列为空，则等待直到有项可用。

如果队列已关闭且为空，或者队列已被立即关闭，则抛出 `QueueShutDown`。

#### get_nowait()

如果立即可用，则返回一个项；否则抛出 `QueueEmpty`。

如果队列已关闭且为空，则抛出 `QueueShutDown`。

#### async join()

阻塞直到队列中的所有项都已接收并处理。

每当向队列中添加一个项时，未完成任务计数会增加。每当消费者协程调用 `task_done()` 表示该项已被取出并且其所有工作已完成时，计数会减少。当未完成任务计数降为零时，`join()` 解除阻塞。

#### async put()

```py
async put(item)
```

将项放入队列。如果队列已满，则等待有空闲槽位后再添加该项。

如果队列已关闭，则抛出 `QueueShutDown`。

#### put_nowait()

```py
put_nowait(item)
```

将项放入队列而不阻塞。

如果没有立即可用的空闲槽位，则抛出 `QueueFull`。

如果队列已关闭，则抛出 `QueueShutDown`。

#### qsize()

返回队列中的项数。

#### shutdown()

```py
shutdown(immediate=False)
```

将 `Queue` 实例置于关闭模式。

队列不能再增长。后续调用 `put()` 将抛出 `QueueShutDown`。当前被阻塞的 `put()` 调用者将被解除阻塞，并在原先等待的任务中抛出 `QueueShutDown`。

如果 `immediate` 为 false（默认值），可以通过 `get()` 调用正常逐步关闭队列，以取出已经加载的任务。

并且如果对每个剩余任务调用 `task_done()`，挂起的 `join()` 将正常解除阻塞。

一旦队列为空，后续调用 `get()` 将抛出 `QueueShutDown`。

如果 `immediate` 为 true，则立即终止队列。队列会被排空至完全为空，并且未完成任务计数会减去被排空的任务数。如果未完成任务数为零，`join()` 的调用者会解除阻塞。此外，被阻塞的 `get()` 调用者会解除阻塞，并由于队列为空而抛出 `QueueShutDown`。

将 `join()` 与 `immediate` 设为 true 一起使用时要谨慎。即使尚未对任务执行任何工作，这也会解除 join 阻塞，违反加入队列的通常不变式。

**3.13 版本新增。**

#### task_done()

表示先前入队的工作项已完成。

由队列消费者使用。对于每次用于获取工作项的 `get()`，随后调用 `task_done()` 会告诉队列该工作项的处理已完成。

如果当前有 `join()` 正在阻塞，则当所有项都已处理完毕（意味着对于每个已 `put()` 到队列中的项都收到了 `task_done()` 调用）时，它将恢复。

如果调用次数多于放入队列中的项数，则抛出 `ValueError`。

## 优先队列

### class asyncio.PriorityQueue

`Queue` 的一个变体；按优先级顺序（最低优先）取出条目。

条目通常是形如 `(priority_number, data)` 的元组。

## LIFO 队列

### class asyncio.LifoQueue

`Queue` 的一个变体，最先取出最近添加的条目（后进先出）。

## 异常

### exception asyncio.QueueEmpty

当对空队列调用 `get_nowait()` 方法时抛出此异常。

### exception asyncio.QueueFull

当对已达到 `maxsize` 的队列调用 `put_nowait()` 方法时抛出此异常。

### exception asyncio.QueueShutDown

当对已关闭的队列调用 `put()`、`put_nowait()`、`get()` 或 `get_nowait()` 时抛出此异常。

**3.13 版本新增。**

## 示例

队列可用于在多个并发任务之间分配工作负载：

```py
import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # 从队列中取出一个“工作项”。
        sleep_for = await queue.get()

        # 休眠 "sleep_for" 秒。
        await asyncio.sleep(sleep_for)

        # 通知队列该“工作项”已处理完毕。
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # 创建一个队列，用于存储我们的“工作负载”。
    queue = asyncio.Queue()

    # 生成随机时长并将它们放入队列。
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # 创建三个 worker 任务以并发处理队列。
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # 等待队列完全处理完毕。
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # 取消我们的 worker 任务。
    for task in tasks:
        task.cancel()
    # 等待所有 worker 任务被取消。
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())
```