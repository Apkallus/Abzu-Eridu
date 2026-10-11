# 协程与任务

https://docs.python.org/zh-cn/3.14/library/asyncio-task.html

async 设置未兑现操作，await 等待操作完成

- `asyncio.Semaphore(value=1)`  
    设置协程任务信号量

    ```py
    sem = asyncio.Semaphore(10)

    # 使用信号量同步
    async with sem:
        # 同步执行的内容
    ```
- `create_task()`
    立即执行协程，并返回一个 Task 对象。

- `await gather()`  
    聚合多个协程或 Future 对象的结果，返回一个汇总结果的 Future 对象。协程会被自动包装成 Future 并调度到事件循环中执行，但不保证调度顺序与传入顺序一致。

- `await asyncio.sleep()`
    非阻塞的暂停当前协程（秒）

- `await open_connection()`  
    异步建立 TCP 连接，返回 `(reader, writer)`
    - `reader` 用 `await reader.read(n)` 读取
    - `writer` 用 `writer.write(...)` + `await writer.drain()` 写入    
        - `writer.close()`  发起关闭
        - `await writer.wait_closed()` 等待关闭真正完成（缓冲刷出/FIN 发送/传输层状态清理等）

- `asyncio.run()`
    运行协程函数

## 并发地运行任务

### `asyncio.gather`

```python
awaitable asyncio.gather(*aws, return_exceptions=False)
```

*并发* 运行 *aws* 序列中的 [可等待对象]。

如果 *aws* 中的某个可等待对象为协程，它将自动被作为一个任务调度。

如果所有可等待对象都成功完成，结果将是一个由所有返回值聚合而成的列表。结果值的顺序与 *aws* 中可等待对象的顺序一致。

如果 *return_exceptions* 为 `False`（默认），所引发的首个异常会立即传播给等待 `gather()` 的任务。*aws* 序列中的其他可等待对象 **不会被取消** 并将继续运行。

如果 *return_exceptions* 为 `True`，异常会和成功的结果一样处理，并聚合至结果列表。

如果 `gather()` *被取消*，所有被提交（尚未完成）的可等待对象也会 *被取消*。

如果 *aws* 序列中的任一 Task 或 Future 对象 *被取消*，它将被当作引发了 `CancelledError` 一样处理——在此情况下 `gather()` 调用 **不会** 被取消。这是为了防止一个已提交的 Task/Future 被取消导致其他 Tasks/Future 也被取消。

> **备注**
> 一个创建、并发地运行任务并等待它们完成的新选择是 `asyncio.TaskGroup`。*TaskGroup* 针对嵌套子任务的调度提供比 *gather* 更强的安全保证：如果一个任务（或子任务，即由某个任务调度的任务）引发了异常，*TaskGroup* 将取消剩余的已排期任务，而 *gather* 不会这样做。

示例：

```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

async def main():
    # *并发地* 调度这三次调用：
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)

asyncio.run(main())

# 预期的输出：
#
#     Task A: Compute factorial(2), currently i=2...
#     Task B: Compute factorial(3), currently i=2...
#     Task C: Compute factorial(4), currently i=2...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3), currently i=3...
#     Task C: Compute factorial(4), currently i=3...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4), currently i=4...
#     Task C: factorial(4) = 24
#     [2, 6, 24]
```

> **备注**
> 如果 *return_exceptions* 为假值，则在 `gather()` 被标记为完成后取消它将不会取消任何已提交的可等待对象。例如，在将一个异常传播给调用者之后，`gather` 可被标记为已完成，因此，在从 `gather` 捕获一个（由可等待对象所引发的）异常之后调用 `gather.cancel()` 将不会取消任何其他可等待对象。

在 3.7 版本发生变更：如果 *gather* 本身被取消，则无论 *return_exceptions* 取值为何，取消都会被传播。

在 3.10 版本发生变更：移除了 *loop* 形参。

自 3.10 版本弃用：如果未提供位置参数或者并非所有位置参数均为 Future 类对象并且没有正在运行的事件循环则会发出弃用警告。

## 在线程中运行

### ♾️ `asyncio.to_thread` —— 将阻塞函数转换为协程

```python
async asyncio.to_thread(func, /, *args, **kwargs)
```

在不同的线程中异步地运行函数 *func*。

> 常用来在现有阻塞函数中简单转为协程

向此函数提供的任何 `*args` 和 `**kwargs` 会被直接传给 *func*。并且，当前 `contextvars.Context` 会被传播，允许在不同的线程中访问来自事件循环的上下文变量。

返回一个可被等待以获取 *func* 的最终结果的协程。

这个协程函数主要是用于执行在其他情况下会阻塞事件循环的 IO 密集型函数/方法。例如：

```python
def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # 请注意 time.sleep() 可被替换为任意一种
    # 阻塞式 IO 密集型操作，例如文件操作。
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")

async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

# 预期的输出：
#
# started main at 19:50:53
# start blocking_io at 19:50:53
# blocking_io complete at 19:50:54
# finished main at 19:50:54
```

在任何协程中直接调用 `blocking_io()` 将会在调用期间阻塞事件循环，导致额外的 1 秒运行时间。但是，通过改用 `asyncio.to_thread()`，我们可以在单独的线程中运行它从而不会阻塞事件循环。

> **备注**
> 由于 `GIL` 的存在，`asyncio.to_thread()` 通常只能被用来将 IO 密集型函数变为非阻塞的。但是，对于会释放 GIL 的扩展模块或无此限制的替代性 Python 实现来说，`asyncio.to_thread()` 也可被用于 CPU 密集型函数。

在 3.9 版本新增。


