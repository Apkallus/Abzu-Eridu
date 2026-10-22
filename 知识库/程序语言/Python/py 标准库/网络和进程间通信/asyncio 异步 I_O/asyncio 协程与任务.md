# 协程与任务

https://docs.python.org/3.15/library/asyncio-task.html

本节概述用于处理协程和任务的高级 asyncio API。

- [`await open_connection()`](https://docs.python.org/zh-cn/3.15/library/asyncio-stream.html)
    异步建立 TCP 连接，返回 `(reader, writer)`
    - `reader` 用 `await reader.read(n)` 读取
    - `writer` 用 `writer.write(...)` + `await writer.drain()` 写入    
        - `writer.close()`  发起关闭
        - `await writer.wait_closed()` 等待关闭真正完成（缓冲刷出/FIN 发送/传输层状态清理等）

## 协程

**源代码：** [Lib/asyncio/coroutines.py](https://github.com/python/cpython/tree/3.15/Lib/asyncio/coroutines.py)

---

使用 `async`/`await` 语法声明的[协程]是编写 asyncio 应用程序的首选方式。例如，以下代码片段打印“hello”，等待 1 秒，然后打印“world”：

```py
>>> import asyncio

>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')

>>> asyncio.run(main())
hello
world
```

注意，仅调用协程不会将其调度执行：

```py
>>> main()
<coroutine object main at 0x1053bb7c8>
```

要实际运行协程，asyncio 提供以下机制：

- `asyncio.run()` 函数用于运行顶层入口 `main()` 函数（见上例）。  
- 等待一个协程。以下代码片段会在等待 1 秒后打印“hello”，然后再等待 *另外* 2 秒后打印“world”：  
  ```py
  import asyncio
  import time

  async def say_after(delay, what):
      await asyncio.sleep(delay)
      print(what)

  async def main():
      print(f"started at {time.strftime('%X')}")

      await say_after(1, 'hello')
      await say_after(2, 'world')

      print(f"finished at {time.strftime('%X')}")

  asyncio.run(main())
  ```
  
  预期输出：
  
  ```text
  started at 17:13:52
  hello
  world
  finished at 17:13:55
  ```

- `asyncio.create_task()` 函数用于将协程作为 asyncio Task 并发运行。  
  让我们修改上面的示例，*并发*运行两个 `say_after` 协程：
  
  ```py
  async def main():
      task1 = asyncio.create_task(
          say_after(1, 'hello'))

      task2 = asyncio.create_task(
          say_after(2, 'world'))

      print(f"started at {time.strftime('%X')}")

      # 等待两个任务完成（大约需要 2 秒。）
      await task1
      await task2

      print(f"finished at {time.strftime('%X')}")
  ```
  
  注意，现在的预期输出显示该代码片段比之前快 1 秒：
  
  ```text
  started at 17:14:32
  hello
  world
  finished at 17:14:34
  ```

- `asyncio.TaskGroup` 类提供了比 `create_task()` 更现代的替代方案。使用此 API，上一个示例变为：
  
  ```py
  async def main():
      async with asyncio.TaskGroup() as tg:
          task1 = tg.create_task(
              say_after(1, 'hello'))

          task2 = tg.create_task(
              say_after(2, 'world'))

          print(f"started at {time.strftime('%X')}")

      # 上下文管理器退出时，await 是隐式的。

      print(f"finished at {time.strftime('%X')}")
  ```
  
  计时和输出应与上一版本相同。
  
  **3.11 版本新增：** `asyncio.TaskGroup`。

## 可等待对象

如果对象可用于 `await` 表达式，我们就说它是**可等待对象**。许多 asyncio API 被设计为接受可等待对象。

*可等待对象*主要有三种类型：**协程**、**Task** 和 **Future**。

### 协程

Python 协程是*可等待对象*，因此可以在其他协程中等待：

```py
import asyncio

async def nested():
    return 42

async def main():
    # 仅调用 "nested()" 不会发生任何事情。
    # 会创建一个协程对象，但没有等待它，
    # 因此它 *根本不会运行*。
    nested()  # 将引发 "RuntimeWarning"。

    # 现在换一种方式，等待它：
    print(await nested())  # 将打印 "42"。

asyncio.run(main())
```

> **重要**
>
> 在本文档中，术语“协程”可用于两个密切相关的概念：
>
> - 一个 *协程函数*：一个 `async def` 函数；
> - 一个 *协程对象*：调用 *协程函数* 返回的对象。

### 任务

*Task* 用于*并发*调度协程。

当使用 `asyncio.create_task()` 等函数将协程包装为 Task 时，协程会自动被调度为很快运行：

```py
import asyncio

async def nested():
    return 42

async def main():
    # 调度 nested() 与 "main()" 并发地很快运行。
    task = asyncio.create_task(nested())

    # "task" 现在可用于取消 "nested()"，
    # 或者只需等待它，直到其完成：
    await task

asyncio.run(main())
```

### Futures

`Future` 是一种特殊的**低层**可等待对象，表示异步操作的**最终结果**。

等待 Future 对象意味着协程将等待，直到该 Future 在其他地方被解决。

asyncio 中的 Future 对象用于让基于回调的代码与 `async`/`await` 一起使用。

通常，**无需**在应用层代码中创建 Future 对象。

库和某些 asyncio API 有时会暴露 Future 对象，它们可以被等待：

```py
async def main():
    await function_that_returns_a_future_object()

    # 这也是有效的：
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
```

返回 Future 对象的低层函数的一个好例子是 `loop.run_in_executor()`。

## 创建任务

**源代码：** [Lib/asyncio/tasks.py](https://github.com/python/cpython/tree/3.15/Lib/asyncio/tasks.py)

---

### asyncio.create_task()

```py
asyncio.create_task(coro, *, name=None, context=None, eager_start=None, **kwargs)
```

将 `coro` 协程包装为 Task 并调度其执行。返回该 Task 对象。

完整函数签名与 Task 构造函数（或工厂）大体相同——此函数的所有关键字参数都会传递到该接口。

可选的关键字专用 `context` 参数允许为 `coro` 指定自定义 `contextvars.Context` 以在其中运行。未提供 `context` 时，会创建当前上下文的副本。

可选的关键字专用 `eager_start` 参数允许指定任务是在调用 `create_task` 期间立即执行，还是稍后调度。如果未传入 `eager_start`，将使用 `loop.set_task_factory()` 设置的模式。

任务在 `get_running_loop()` 返回的事件循环中执行；如果当前线程没有正在运行的事件循环，则抛出 `RuntimeError`。

> **注意**
>
> `asyncio.TaskGroup.create_task()` 是一个利用结构化并发的新替代方案；它允许等待一组相关任务，并提供强安全保证。

> **重要**
>
> 保存对此函数结果的引用，以避免任务在执行中途消失。事件循环只保留对任务的弱引用。未在其他地方引用的任务可能随时被垃圾回收，甚至在其完成之前。对于可靠的“触发后不管”后台任务，请将它们收集到一个集合中：
>
> ```py
> background_tasks = set()
>
> for i in range(10):
>     task = asyncio.create_task(some_coro(param=i))
>
>     # 将任务添加到集合中。这会创建强引用。
>     background_tasks.add(task)
>
>     # 为防止永远保留对已完成任务的引用，
>     # 让每个任务在完成后从集合中移除自己的引用：
>     task.add_done_callback(background_tasks.discard)
> ```
>
> 注意，此方法从不等待任务，因此如果任务失败，其异常永远不会被获取，并且当任务被垃圾回收时，asyncio 会记录一条“Task exception was never retrieved”消息。为避免此问题，请使用 `asyncio.TaskGroup`，它会保留对每个任务的强引用、等待它们并传播其异常：
>
> ```py
> async with asyncio.TaskGroup() as tg:
>     for i in range(10):
>         tg.create_task(some_coro(param=i))
> ```

**3.7 版本新增。**

**3.8 版本变更：** 添加了 `name` 参数。

**3.11 版本变更：** 添加了 `context` 参数。

**3.14 版本变更：** 通过传递所有 `kwargs`，添加了 `eager_start` 参数。

## 任务取消

任务可以轻松且安全地被取消。任务被取消时，下一次机会会在该任务中抛出 `asyncio.CancelledError`。

建议协程使用 `try/finally` 块来稳健地执行清理逻辑。如果显式捕获了 `asyncio.CancelledError`，通常应在清理完成后传播它。`asyncio.CancelledError` 直接继承自 `BaseException`，因此大多数代码无需感知它。

启用结构化并发的 asyncio 组件（如 `asyncio.TaskGroup` 和 `asyncio.timeout()`）内部使用取消来实现；如果协程吞掉 `asyncio.CancelledError`，这些组件可能行为异常。类似地，用户代码通常不应调用 `uncancel`。不过，如果确实希望抑制 `asyncio.CancelledError`，还必须调用 `uncancel()` 以完全移除取消状态。

## 任务组

任务组将任务创建 API 与一种方便可靠的方式结合起来，用于等待组内所有任务完成。

### class asyncio.TaskGroup

一个持有任务组的异步上下文管理器。可以使用 `create_task()` 将任务添加到组中。当上下文管理器退出时，会等待所有任务。

**3.11 版本新增。**

#### create_task()

```py
create_task(coro, *, name=None, context=None, eager_start=None, **kwargs)
```

在此任务组中创建一个任务。签名与 `asyncio.create_task()` 匹配。如果任务组处于非活动状态（例如尚未进入、已经完成或正在关闭），我们将关闭给定的 `coro` 并抛出 `RuntimeError`。

**3.13 版本变更：** 如果任务组不活动，则关闭给定协程。

**3.14 版本变更：** 将所有 `kwargs` 传递给 `loop.create_task()`。

#### cancel()

取消任务组。这是任务组生命周期的非异常提前退出——当组的目标已达成或其服务不再需要时很有用。

将对组内尚未完成的任何任务以及组的父级（主体）调用 `cancel()`。任务组上下文管理器将退出，且不会抛出 `asyncio.CancelledError`。

如果在进入任务组之前调用 `cancel()`，该组将在进入时被取消。这对于某些模式很有用：一段代码将未使用的 `asyncio.TaskGroup` 实例传递给另一段代码，以便能够取消组内运行的任何内容。

`cancel()` 是幂等的，并且可以在任务组已经退出后调用。

使用 `cancel()` 的一些方式：

- 根据某些条件或事件从任务组主体中调用它
- 通过 `create_task()` 将任务组实例传递给子任务，允许子任务有条件地取消整个组
- 在打开任务组*之前*，将任务组实例或绑定的 `cancel()` 方法传递给其他任务，允许远程取消

**3.15 版本新增。**

示例：

```py
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coro(...))
        task2 = tg.create_task(another_coro(...))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
```

`async with` 语句将等待组内所有任务完成。在等待期间，仍可以向组中添加新任务（例如，将 `tg` 传入某个协程，并在该协程中调用 `tg.create_task()`）。还可以根据某些条件，通过 `tg.cancel()` 请求终止整个任务组。一旦最后一个任务完成并且退出 `async with` 块，就不得再向组中添加新任务。

当组内任一任务首次因 `asyncio.CancelledError` 以外的异常而失败时，组内剩余任务会被取消。此后不能再向组中添加任务。此时，如果 `async with` 语句的主体仍处于活动状态（即尚未调用 `__aexit__()`），则直接包含该 `async with` 语句的任务也会被取消。产生的 `asyncio.CancelledError` 会中断 `await`，但不会冒泡出包含它的 `async with` 语句。

所有任务完成后，如果有任何任务因 `asyncio.CancelledError` 以外的异常而失败，这些异常会合并到一个 `ExceptionGroup` 或 `BaseExceptionGroup`（视情况而定；参见其文档）中，然后抛出。

有两种基异常会被特殊处理：如果任何任务因 `KeyboardInterrupt` 或 `SystemExit` 失败，任务组仍会取消剩余任务并等待它们，但随后会重新抛出最初的 `KeyboardInterrupt` 或 `SystemExit`，而不是 `ExceptionGroup` 或 `BaseExceptionGroup`。

如果 `async with` 语句的主体因异常退出（因此调用 `__aexit__()` 时设置了异常），这会被视为与某个任务失败相同：剩余任务被取消并等待，非取消异常会被分组到一个异常组中并抛出。传入 `__aexit__()` 的异常（除非是 `asyncio.CancelledError`）也会包含在异常组中。对于 `KeyboardInterrupt` 和 `SystemExit`，与上一段相同，也有同样的特殊情况。还有一个仅针对 `async with` 主体的额外特殊情况：如果它抛出 `GeneratorExit`，并且其他任务都没有抛出会被报告的异常，则重新抛出 `GeneratorExit`。

任务组会小心避免将用于“唤醒”其 `__aexit__()` 的内部取消与其他方对运行该任务组的任务发出的取消请求混淆。特别是，当一个任务组在语法上嵌套在另一个任务组中，并且两者同时在其某个子任务中遇到异常时，内层任务组会处理其异常，然后外层任务组会收到另一次取消并处理自己的异常。

如果任务组被外部取消并且还必须抛出 `ExceptionGroup`，它将调用父任务的 `cancel()` 方法。这确保在下一次 `await` 时抛出 `asyncio.CancelledError`，因此取消不会丢失。

任务组会保留 `asyncio.Task.cancelling()` 报告的取消计数。

**3.13 版本变更：** 改进同时发生的内部和外部取消的处理，并正确保留取消计数。

**3.15 版本变更：** 添加针对 `GeneratorExit` 的特殊情况。

## 休眠

### async asyncio.sleep()

```py
async asyncio.sleep(delay, result=None)
```

阻塞 `delay` 秒。

如果提供了 `result`，则在协程完成时将其返回给调用者。

`sleep()` 总是挂起当前任务，允许其他任务运行。

将延迟设为 0 提供了一条优化路径，以允许其他任务运行。长时间运行的函数可以用它来避免在函数调用的整个持续时间内阻塞事件循环。

示例：每秒钟显示当前日期，持续 5 秒的协程：

```py
import asyncio
import datetime as dt

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(dt.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
```

**3.10 版本变更：** 移除了 `loop` 参数。

**3.13 版本变更：** 如果 `delay` 为 `nan`，则抛出 `ValueError`。

## 并发运行任务

### awaitable asyncio.gather()

```py
awaitable asyncio.gather(*aws, return_exceptions=False)
```

*并发*运行 `aws` 序列中的可等待对象。

如果 `aws` 中的任何可等待对象是协程，它会自动被调度为 Task。

如果所有可等待对象都成功完成，结果是一个聚合的返回值列表。结果值的顺序与 `aws` 中可等待对象的顺序对应。

如果 `return_exceptions` 为 `False`（默认值），第一个抛出的异常会立即传播给等待 `gather()` 的任务。`aws` 序列中的其他可等待对象**不会被取消**，并会继续运行。

如果 `return_exceptions` 为 `True`，异常会被视为与成功结果相同，并聚合到结果列表中。

如果 `gather()` 被*取消*，所有已提交的可等待对象（尚未完成的）也会被*取消*。

如果 `aws` 序列中的任何 Task 或 Future 被*取消*，它会被视为抛出了 `CancelledError`——在这种情况下，`gather()` 调用**不会**被取消。这是为了防止取消一个已提交的 Task/Future 导致其他 Task/Future 被取消。

> **注意**
>
> 并发创建和运行任务并等待其完成的新替代方案是 `asyncio.TaskGroup`。对于调度嵌套子任务，*TaskGroup* 比 *gather* 提供更强的安全保证：如果某个任务（或子任务，即由任务调度的任务）抛出异常，*TaskGroup* 会取消剩余已调度的任务，而 *gather* 不会。

示例：

```py
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
    # 并发调度三次调用：
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)

asyncio.run(main())

# 预期输出：
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

> **注意**
>
> 如果 `return_exceptions` 为 false，在 `gather()` 被标记为完成后取消它不会取消任何已提交的可等待对象。例如，`gather` 可以在将异常传播给调用者后被标记为完成，因此，在从 `gather` 捕获异常（由其中一个可等待对象抛出）后调用 `gather.cancel()` 不会取消任何其他可等待对象。

**3.7 版本变更：** 如果 *gather* 本身被取消，则无论 `return_exceptions` 如何，取消都会传播。

**3.10 版本变更：** 移除了 `loop` 参数。

**3.10 起弃用：** 如果未提供位置参数，或者并非所有位置参数都是 Future 类对象，并且没有正在运行的事件循环，则会发出弃用警告。

## 急切任务工厂

### asyncio.eager_task_factory()

```py
asyncio.eager_task_factory(loop, coro, *, name=None, context=None)
```

用于急切执行任务的任务工厂。

使用此工厂时（通过 `loop.set_task_factory(asyncio.eager_task_factory)`），协程会在 `Task` 构造期间同步开始执行。任务只有在阻塞时才会被调度到事件循环。由于同步完成的协程避免了循环调度的开销，这可以提升性能。

一个常见的有益示例是使用缓存或记忆化来尽可能避免实际 I/O 的协程。

> **注意**
>
> 立即执行协程是一种语义变更。如果协程返回或抛出异常，任务永远不会被调度到事件循环。如果协程执行阻塞，任务会被调度到事件循环。此变更可能给现有应用程序带来行为变化。例如，应用程序的任务执行顺序很可能发生变化。

**3.12 版本新增。**

### asyncio.create_eager_task_factory()

```py
asyncio.create_eager_task_factory(custom_task_constructor)
```

创建一个急切任务工厂，类似于 `eager_task_factory()`，但在创建新任务时使用提供的 `custom_task_constructor`，而不是默认的 `Task`。

`custom_task_constructor` 必须是一个可调用对象，其签名与 `Task.__init__` 的签名匹配。该可调用对象必须返回一个与 `asyncio.Task` 兼容的对象。

此函数返回一个可调用对象，旨在通过 `loop.set_task_factory(factory)` 用作事件循环的任务工厂。

**3.12 版本新增。**

## 防止取消

### awaitable asyncio.shield()

```py
awaitable asyncio.shield(aw)
```

保护一个可等待对象不被取消。

如果 `aw` 是协程，它会自动被调度为 Task。

语句：

```py
task = asyncio.create_task(something())
res = await shield(task)
```

等价于：

```py
res = await something()
```

*除了*如果包含它的协程被取消，运行在 `something()` 中的 Task 不会被取消。从 `something()` 的角度来看，取消没有发生。尽管其调用者仍被取消，因此 `await` 表达式仍会抛出 `CancelledError`。

如果 `something()` 通过其他方式被取消（即从其内部取消），那也会取消 `shield()`。

如果希望完全忽略取消（不推荐），应将 `shield()` 函数与 `try`/`except` 子句结合使用，如下所示：

```py
task = asyncio.create_task(something())
try:
    res = await shield(task)
except CancelledError:
    res = None
```

> **重要**
>
> 保存对此函数传入的任务的引用，以避免任务在执行中途消失。事件循环只保留对任务的弱引用。未在其他地方引用的任务可能随时被垃圾回收，甚至在其完成之前。

**3.10 版本变更：** 移除了 `loop` 参数。

**3.10 起弃用：** 如果 `aw` 不是 Future 类对象，并且没有正在运行的事件循环，则会发出弃用警告。

## 超时

### asyncio.timeout()

```py
asyncio.timeout(delay)
```

返回一个异步上下文管理器，可用于限制等待某事物所花费的时间。

`delay` 可以是 `None`，也可以是等待的秒数（float/int）。如果 `delay` 为 `None`，则不会应用时间限制；如果在创建上下文管理器时延迟未知，这会很有用。

无论哪种情况，都可以在创建后使用 `Timeout.reschedule()` 重新调度该上下文管理器。

示例：

```py
async def main():
    async with asyncio.timeout(10):
        await long_running_task()
```

如果 `long_running_task` 完成所需时间超过 10 秒，上下文管理器将取消当前任务，并在内部处理产生的 `asyncio.CancelledError`，将其转换为可捕获和处理的 `TimeoutError`。

> **注意**
>
> `asyncio.timeout()` 上下文管理器负责将 `asyncio.CancelledError` 转换为 `TimeoutError`，这意味着 `TimeoutError` 只能在上下文管理器*外部*捕获。

捕获 `TimeoutError` 的示例：

```py
async def main():
    try:
        async with asyncio.timeout(10):
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")
```

`asyncio.timeout()` 产生的上下文管理器可以重新调度到不同的截止时间，并可以检查。

### class asyncio.Timeout()

```py
class asyncio.Timeout(when)
```

用于取消逾期协程的异步上下文管理器。

优先使用 `asyncio.timeout()` 或 `asyncio.timeout_at()`，而不是直接实例化 `Timeout`。

`when` 应是上下文应超时的绝对时间，以事件循环的时钟为度量：

- 如果 `when` 为 `None`，超时永远不会触发。
- 如果 `when < loop.time()`，超时将在事件循环的下一次迭代中触发。

#### when() → float | None

返回当前截止时间，如果未设置当前截止时间，则返回 `None`。

#### reschedule()

```py
reschedule(when: float | None)
```

重新调度超时。

#### expired() → bool

返回上下文管理器是否已超过其截止时间（已过期）。

示例：

```py
async def main():
    try:
        # 启动时我们不知道超时时间，因此传入 ``None``。
        async with asyncio.timeout(None) as cm:
            # 现在我们知道超时时间了，因此重新调度它。
            new_deadline = get_running_loop().time() + 10
            cm.reschedule(new_deadline)

            await long_running_task()
    except TimeoutError:
        pass

    if cm.expired():
        print("Looks like we haven't finished on time.")
```

超时上下文管理器可以安全地嵌套。

**3.11 版本新增。**

### asyncio.timeout_at()

```py
asyncio.timeout_at(when)
```

类似于 `asyncio.timeout()`，不同之处在于 `when` 是停止等待的绝对时间，或 `None`。

示例：

```py
async def main():
    loop = get_running_loop()
    deadline = loop.time() + 20
    try:
        async with asyncio.timeout_at(deadline):
            await long_running_task()
    except TimeoutError:
        print("The long operation timed out, but we've handled it.")

    print("This statement will run regardless.")
```

**3.11 版本新增。**

### async asyncio.wait_for()

```py
async asyncio.wait_for(aw, timeout)
```

等待 `aw` 可等待对象在超时情况下完成。

`timeout` 可以是 `None`，也可以是等待的秒数（float 或 int）。如果 `timeout` 为 `None`，则阻塞直到 future 完成。

如果发生超时，它会取消 `aw` 并抛出 `TimeoutError`。

要防止 `aw` 被取消，请将其包装在 `shield()` 中。

该函数会等待直到 future 实际被取消，因此总等待时间可能超过 `timeout`。如果取消期间发生异常，则会传播该异常。

如果等待被取消，future `aw` 也会被取消。

示例：

```py
async def eternity():
    # 休眠一小时
    await asyncio.sleep(3600)
    print('yay!')

async def main():
    # 最多等待 1 秒
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except TimeoutError:
        print('timeout!')

asyncio.run(main())

# 预期输出：
#
#     timeout!
```

**3.7 版本变更：** 当 `aw` 因超时被取消时，`wait_for` 会等待 `aw` 被取消。以前，它会立即抛出 `TimeoutError`。

**3.10 版本变更：** 移除了 `loop` 参数。

**3.11 版本变更：** 抛出 `TimeoutError`，而不是 `asyncio.TimeoutError`。

**3.12 版本变更：** 使用 `asyncio.timeout()` 实现；当 `timeout` 为正数时，作为 `aw` 传入的协程不再被包装在 `Task` 中。

## 等待原语

### async asyncio.wait()

```py
async asyncio.wait(aws, *, timeout=None, return_when=ALL_COMPLETED)
```

并发运行 `aws` 可迭代对象中的 `Future` 和 `Task` 实例，并阻塞直到 `return_when` 指定的条件。

`aws` 可迭代对象不能为空。

返回两组 Task/Future：`(done, pending)`。

用法：

```py
done, pending = await asyncio.wait(aws)
```

`timeout`（float 或 int，如果指定）可用于控制返回前等待的最大秒数。

注意，此函数不会抛出 `TimeoutError`。超时发生时尚未完成的 Future 或 Task 只会简单地在第二组中返回。

`return_when` 指示此函数应在何时返回。它必须是以下常量之一：

- `asyncio.FIRST_COMPLETED`：当任意 future 完成或被取消时，函数将返回。
- `asyncio.FIRST_EXCEPTION`：当任意 future 因抛出异常而完成时，函数将返回。如果没有 future 抛出异常，则等价于 `ALL_COMPLETED`。
- `asyncio.ALL_COMPLETED`：当所有 future 完成或被取消时，函数将返回。

与 `wait_for()` 不同，`wait()` 在发生超时时不会取消 futures。

如果 `wait()` 被取消，`aws` 中的 futures 不会被取消，并会继续运行。

**3.10 版本变更：** 移除了 `loop` 参数。

**3.11 版本变更：** 禁止将协程对象直接传给 `wait()`。

**3.12 版本变更：** 添加对生成任务的生成器的支持。

### asyncio.as_completed()

```py
asyncio.as_completed(aws, *, timeout=None)
```

并发运行 `aws` 可迭代对象中的可等待对象。返回的对象可以被迭代，以在可等待对象完成时获取它们的结果。

`as_completed()` 返回的对象可以按异步迭代器或普通迭代器进行迭代。使用异步迭代时，如果最初提供的可等待对象是任务或 future，则会产出它们。这使得将先前调度的任务与其结果关联起来变得容易。示例：

```py
ipv4_connect = create_task(open_connection("127.0.0.1", 80))
ipv6_connect = create_task(open_connection("::1", 80))
tasks = [ipv4_connect, ipv6_connect]

async for earliest_connect in as_completed(tasks):
    # earliest_connect 已完成。结果可以通过等待它
    # 或调用 earliest_connect.result() 获得。
    reader, writer = await earliest_connect

    if earliest_connect is ipv6_connect:
        print("IPv6 connection established.")
    else:
        print("IPv4 connection established.")
```

在异步迭代期间，对于提供的不是任务或 future 的可等待对象，会产出隐式创建的任务。

当作为普通迭代器使用时，每次迭代都会产出一个新协程，该协程返回下一个完成的可等待对象的结果或抛出其异常。此模式与低于 3.13 的 Python 版本兼容：

```py
ipv4_connect = create_task(open_connection("127.0.0.1", 80))
ipv6_connect = create_task(open_connection("::1", 80))
tasks = [ipv4_connect, ipv6_connect]

for next_connect in as_completed(tasks):
    # next_connect 不是原始任务对象之一。必须等待它，
    # 以获取下一个完成的可等待对象的结果值或抛出其异常。
    reader, writer = await next_connect
```

如果超时在所有可等待对象完成之前发生，则会抛出 `TimeoutError`。这由异步迭代期间的 `async for` 循环或普通迭代期间产出的协程抛出。

`as_completed()` 不会取消运行所提供可等待对象的任务：如果发生超时或迭代被取消，剩余任务会继续运行。

**3.10 版本变更：** 移除了 `loop` 参数。

**3.10 起弃用：** 如果 `aws` 可迭代对象中并非所有可等待对象都是 Future 类对象，并且没有正在运行的事件循环，则会发出弃用警告。

**3.12 版本变更：** 添加对生成任务的生成器的支持。

**3.13 版本变更：** 结果现在既可用作异步迭代器，也可用作普通迭代器（以前它只是普通迭代器）。

## 在线程中运行

### 🛠️ async asyncio.to_thread()

```py
async asyncio.to_thread(func, /, *args, **kwargs)
```

在单独的线程中异步运行函数 `func`。

> 可用来在现有阻塞函数中简单转为协程


为此函数提供的任何 `*args` 和 `**kwargs` 都会直接传递给 `func`。此外，当前 `contextvars.Context` 会被传播，允许在单独线程中访问事件循环线程的上下文变量。

返回一个协程，可以等待它来获取 `func` 的最终结果。

此协程函数主要用于执行 IO 密集型函数/方法；如果它们在主线程中运行，否则会阻塞事件循环。例如：

```py
def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # 注意，time.sleep() 可以替换为任何阻塞的
    # IO 密集型操作，例如文件操作。
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")

async def main():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


asyncio.run(main())

# 预期输出：
#
# started main at 19:50:53
# start blocking_io at 19:50:53
# blocking_io complete at 19:50:54
# finished main at 19:50:54
```

在任何协程中直接调用 `blocking_io()` 都会在其持续时间内阻塞事件循环，导致额外的 1 秒运行时间。相反，通过使用 `asyncio.to_thread()`，我们可以在单独的线程中运行它，而不会阻塞事件循环。

> **注意**
>
> 由于 GIL，`asyncio.to_thread()` 通常只能用于使 IO 密集型函数变为非阻塞。不过，对于释放 GIL 的扩展模块或没有 GIL 的替代 Python 实现，`asyncio.to_thread()` 也可用于 CPU 密集型函数。

**3.9 版本新增。**

## 从其他线程调度

### asyncio.run_coroutine_threadsafe()

```py
asyncio.run_coroutine_threadsafe(coro, loop)
```

将协程提交给给定的事件循环。线程安全。

返回一个 `concurrent.futures.Future`，用于从另一个 OS 线程等待结果。

此函数旨在从与事件循环运行所在的 OS 线程不同的线程中调用。示例：

```py
def in_thread(loop: asyncio.AbstractEventLoop) -> None:
    # 运行一些阻塞 IO
    pathlib.Path("example.txt").write_text("hello world", encoding="utf8")

    # 创建一个协程
    coro = asyncio.sleep(1, result=3)

    # 将协程提交给给定的事件循环
    future = asyncio.run_coroutine_threadsafe(coro, loop)

    # 使用可选的 timeout 参数等待结果
    assert future.result(timeout=2) == 3

async def amain() -> None:
    # 获取正在运行的事件循环
    loop = asyncio.get_running_loop()

    # 在线程中运行一些内容
    await asyncio.to_thread(in_thread, loop)
```

也可以反过来运行。示例：

```py
@contextlib.contextmanager
def loop_in_thread() -> Generator[asyncio.AbstractEventLoop]:
    loop_fut = concurrent.futures.Future[asyncio.AbstractEventLoop]()
    stop_event = asyncio.Event()

    async def main() -> None:
        loop_fut.set_result(asyncio.get_running_loop())
        await stop_event.wait()

    with concurrent.futures.ThreadPoolExecutor(1) as tpe:
        complete_fut = tpe.submit(asyncio.run, main())
        for fut in concurrent.futures.as_completed((loop_fut, complete_fut)):
            if fut is loop_fut:
                loop = loop_fut.result()
                try:
                    yield loop
                finally:
                    loop.call_soon_threadsafe(stop_event.set)
            else:
                fut.result()

# 在另一个线程中创建事件循环
with loop_in_thread() as loop:
    # 创建一个协程
    coro = asyncio.sleep(1, result=3)

    # 将协程提交给给定的事件循环
    future = asyncio.run_coroutine_threadsafe(coro, loop)

    # 使用可选的 timeout 参数等待结果
    assert future.result(timeout=2) == 3
```

如果协程中抛出异常，返回的 Future 会收到通知。它也可以用于取消事件循环中的任务：

```py
try:
    result = future.result(timeout)
except TimeoutError:
    print('The coroutine took too long, cancelling the task...')
    future.cancel()
except Exception as exc:
    print(f'The coroutine raised an exception: {exc!r}')
else:
    print(f'The coroutine returned: {result!r}')
```

请参阅文档中的并发与多线程部分。

与其他 asyncio 函数不同，此函数要求显式传递 `loop` 参数。

**3.5.1 版本新增。**

## 自省

### asyncio.current_task()

```py
asyncio.current_task(loop=None)
```

返回当前正在运行的 `Task` 实例，如果没有任务正在运行，则返回 `None`。

如果 `loop` 为 `None`，则使用 `get_running_loop()` 获取当前事件循环。

**3.7 版本新增。**

### asyncio.all_tasks()

```py
asyncio.all_tasks(loop=None)
```

返回由事件循环运行的尚未完成的 `Task` 对象集合。

如果 `loop` 为 `None`，则使用 `get_running_loop()` 获取当前事件循环。

**3.7 版本新增。**

### asyncio.iscoroutine()

```py
asyncio.iscoroutine(obj)
```

如果 `obj` 是协程对象，则返回 `True`。

**3.4 版本新增。**

## Task 对象

### class asyncio.Task()

```py
class asyncio.Task(coro, *, loop=None, name=None, context=None, eager_start=False)
```

一个运行 Python 协程的 Future 类对象。非线程安全。

Task 用于在事件循环中运行协程。如果协程等待一个 Future，Task 会挂起该协程的执行，并等待该 Future 完成。当 Future *完成*时，被包装协程的执行会恢复。

事件循环使用协作式调度：事件循环一次运行一个 Task。当一个 Task 等待 Future 完成时，事件循环会运行其他 Task、回调或执行 IO 操作。

使用高层 `asyncio.create_task()` 函数创建 Task，或使用低层 `loop.create_task()` 或 `ensure_future()` 函数。不鼓励手动实例化 Task。

要取消正在运行的 Task，请使用 `cancel()` 方法。调用它会导致 Task 向被包装的协程抛出 `CancelledError` 异常。如果协程在取消期间正在等待一个 Future 类对象，则被等待的对象也会被取消。

`cancelled()` 可用于检查 Task 是否被取消。如果被包装的协程没有抑制 `CancelledError` 异常并且实际被取消，该方法返回 `True`。

`asyncio.Task` 从 `Future` 继承了其所有 API，但 `Future.set_result()` 和 `Future.set_exception()` 除外。

可选的关键字专用 `context` 参数允许为 `coro` 指定自定义 `contextvars.Context` 以在其中运行。如果未提供 `context`，Task 会复制当前上下文，并在稍后于复制的上下文中运行其协程。

可选的关键字专用 `eager_start` 参数允许在创建任务时急切开始执行 `asyncio.Task`。如果设为 `True` 且事件循环正在运行，任务将立即开始执行协程，直到协程第一次阻塞。如果协程在没有阻塞的情况下返回或抛出异常，任务将急切完成，并跳过调度到事件循环。

Task 对其包装协程的返回类型是泛型的。

**3.7 版本变更：** 添加对 `contextvars` 模块的支持。

**3.8 版本变更：** 添加了 `name` 参数。

**3.10 起弃用：** 如果未指定 `loop` 并且没有正在运行的事件循环，则会发出弃用警告。

**3.11 版本变更：** 添加了 `context` 参数。

**3.12 版本变更：** 添加了 `eager_start` 参数。

#### done()

如果 Task *完成*，则返回 `True`。

当被包装的协程返回值、抛出异常，或 Task 被取消时，Task 即*完成*。

#### result()

返回 Task 的结果。

如果 Task *完成*，则返回被包装协程的结果（如果协程抛出异常，则重新抛出该异常）。

如果 Task 已被*取消*，此方法抛出 `CancelledError` 异常。

如果 Task 的结果尚不可用，此方法抛出 `InvalidStateError` 异常。

#### exception()

返回 Task 的异常。

如果被包装的协程抛出异常，则返回该异常。如果被包装的协程正常返回，此方法返回 `None`。

如果 Task 已被*取消*，此方法抛出 `CancelledError` 异常。

如果 Task 尚未*完成*，此方法抛出 `InvalidStateError` 异常。

#### add_done_callback()

```py
add_done_callback(callback, *, context=None)
```

添加一个在 Task *完成*时运行的回调。

此方法只应在低层基于回调的代码中使用。

更多细节请参阅 `Future.add_done_callback()` 的文档。

#### remove_done_callback()

```py
remove_done_callback(callback)
```

从回调列表中移除 `callback`。

此方法只应在低层基于回调的代码中使用。

更多细节请参阅 `Future.remove_done_callback()` 的文档。

#### get_stack()

```py
get_stack(*, limit=None)
```

返回此 Task 的栈帧列表。

如果被包装的协程未完成，则返回其挂起处的栈。如果协程已成功完成或被取消，则返回空列表。如果协程因异常而终止，则返回 traceback 帧列表。

帧始终按从旧到新的顺序排列。

对于挂起的协程，只返回一个栈帧。

可选的 `limit` 参数设置要返回的最大帧数；默认返回所有可用帧。返回列表的顺序取决于返回的是栈还是 traceback：返回栈的最新帧，但返回 traceback 的最旧帧。（这与 traceback 模块的行为一致。）

#### print_stack()

```py
print_stack(*, limit=None, file=None)
```

打印此 Task 的栈或 traceback。

这会产生与 traceback 模块类似的输出，用于 `get_stack()` 检索到的帧。

`limit` 参数直接传递给 `get_stack()`。

`file` 参数是写入输出的 I/O 流；默认输出写入 `sys.stdout`。

#### get_coro()

返回由 `Task` 包装的协程对象。

> **注意**
>
> 对于已经急切完成的 Task，这将返回 `None`。参见急切任务工厂。

**3.8 版本新增。**

**3.12 版本变更：** 新增的急切任务执行意味着结果可能为 `None`。

#### get_context()

返回与任务关联的 `contextvars.Context` 对象。

**3.12 版本新增。**

#### get_name()

返回 Task 的名称。

如果没有为 Task 显式分配名称，默认 asyncio Task 实现会在实例化期间生成一个默认名称。

**3.8 版本新增。**

#### set_name()

```py
set_name(value)
```

设置 Task 的名称。

`value` 参数可以是任何对象，然后会被转换为字符串。

在默认 Task 实现中，名称将在任务对象的 `repr()` 输出中可见。

**3.8 版本新增。**

#### cancel()

```py
cancel(msg=None)
```

请求取消 Task。

如果 Task 已经*完成*或*取消*，返回 `False`，否则返回 `True`。

该方法安排在下一次事件循环周期向被包装的协程抛出 `CancelledError` 异常。

然后协程有机会清理，甚至通过使用 `try` … `except CancelledError` … `finally` 块抑制异常来拒绝请求。因此，与 `Future.cancel()` 不同，`Task.cancel()` 不保证 Task 会被取消，尽管完全抑制取消并不常见，并且被积极劝阻。如果协程仍然决定抑制取消，除了捕获异常外，还需要调用 `Task.uncancel()`。

如果正在取消的 Task 当前正在等待一个 Future 类对象，该被等待的对象也会被取消。此取消会沿着整个被等待对象链向下传播。

**3.9 版本变更：** 添加了 `msg` 参数。

**3.11 版本变更：** `msg` 参数从被取消的任务传播到其等待者。

以下示例说明协程如何拦截取消请求：

```py
async def cancel_me():
    print('cancel_me(): before sleep')

    try:
        # 等待 1 小时
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print('cancel_me(): cancel sleep')
        raise
    finally:
        print('cancel_me(): after sleep')

async def main():
    # 创建一个 "cancel_me" Task
    task = asyncio.create_task(cancel_me())

    # 等待 1 秒
    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")

asyncio.run(main())

# 预期输出：
#
#     cancel_me(): before sleep
#     cancel_me(): cancel sleep
#     cancel_me(): after sleep
#     main(): cancel_me is cancelled now
```

#### cancelled()

如果 Task 已*取消*，则返回 `True`。

当使用 `cancel()` 请求取消，并且被包装的协程传播了抛入其中的 `CancelledError` 异常时，Task 即*取消*。

#### uncancel()

递减此 Task 的取消请求计数。

返回剩余的取消请求数。

注意，一旦已取消任务的执行完成，进一步调用 `uncancel()` 将无效。

**3.11 版本新增。**

此方法由 asyncio 内部使用，不期望由最终用户代码使用。特别是，如果 Task 成功取消取消，这允许结构化并发元素（如任务组和 `asyncio.timeout()`）继续运行，将取消隔离到各自的结构化块。例如：

```py
async def make_request_with_timeout():
    try:
        async with asyncio.timeout(1):
            # 受超时影响的结构化块：
            await make_request()
            await make_another_request()
    except TimeoutError:
        log("There was a timeout")
    # 不受超时影响的外部代码：
    await unrelated_code()
```

虽然包含 `make_request()` 和 `make_another_request()` 的块可能因超时被取消，但 `unrelated_code()` 即使在超时情况下也应继续运行。这是通过 `uncancel()` 实现的。`TaskGroup` 上下文管理器以类似方式使用 `uncancel()`。

如果最终用户代码由于某种原因通过捕获 `CancelledError` 来抑制取消，则需要调用此方法以移除取消状态。

当此方法将取消计数递减到零时，该方法会检查先前的 `cancel()` 调用是否安排了向任务抛出 `CancelledError`。如果尚未抛出，则撤销该安排（通过重置内部 `_must_cancel` 标志）。

**3.13 版本变更：** 更改为在计数达到零时撤销待处理的取消请求。

#### cancelling()

返回此 Task 的待处理取消请求数，即调用 `cancel()` 的次数减去调用 `uncancel()` 的次数。

注意，如果此数字大于零但 Task 仍在执行，`cancelled()` 仍将返回 `False`。这是因为可以通过调用 `uncancel()` 降低此数字，如果取消请求降至零，任务最终可能不会被取消。

此方法由 asyncio 内部使用，不期望由最终用户代码使用。更多细节请参阅 `uncancel()`。

**3.11 版本新增。**