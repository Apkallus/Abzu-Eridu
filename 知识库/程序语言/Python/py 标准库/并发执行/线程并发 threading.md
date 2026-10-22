# threading — 线程并发

https://docs.python.org/3.14/library/threading.html

- `threading.Condition`：
    带锁的全局共享状态变量（锁/阻塞/唤醒）
    - `wait(timeout)` 阻塞直到被 `notify_all()` 唤醒或超时。
    - `wait_for(...)` 等待直到条件满足或超时

- `Event` 对象，线程间通信。
    实现事件对象的类。事件对象管理一个内部标识，调用 `set()` 方法可将其设置为 `true`。调用 `clear()` 方法可将其设置为 `false`。调用 `wait()` 方法将进入阻塞直到标识为 true。这个标识初始时为 `false`（即，初始时阻塞）。
    - 使用此对象也可实现创建所有任务后同时执行

## 介绍

`threading` 模块提供了一种在单个进程中并发运行多个 [线程]（进程的较小单元）的方式。它允许创建和管理线程，使得可以并行执行任务，共享内存空间。当任务受 I/O 限制时，例如文件操作或网络请求，大部分时间都花在等待外部资源上，线程特别有用。

`threading` 的典型用例包括管理工作线程池，可以并发处理多个任务。以下是使用 `Thread` 创建和启动线程的基本示例：

```python
import threading
import time

# 模拟的阻塞型功能
def crawl(link, delay=3):
    print(f"crawl started for {link}")
    time.sleep(delay)  # 阻塞式 I/O（模拟网络请求）
    print(f"crawl ended for {link}")

links = [
    "https://python.org",
    "https://docs.python.org",
    "https://peps.python.org",
]

# 为每个链接启动线程
threads = []
for link in links:
    # 使用 `args` 传递位置参数，使用 `kwargs` 传递关键字参数
    t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
    threads.append(t)

# 启动每个线程
for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
```

在 3.7 版本发生变更：此模块过去是可选的，现在始终可用。

> **参见**
> `concurrent.futures.ThreadPoolExecutor` 提供了更高层级的接口，可将任务推送到后台线程而不会阻塞调用线程的执行，同时仍能在需要时获取其结果。
>
> `queue` 提供了在线程之间交换数据的线程安全接口。
>
> `asyncio` 提供了实现任务级并发的另一种方法，而无需使用多个操作系统线程。

> **备注**
> 在 Python 2.x 系列中，此模块包含一些方法和函数的 `camelCase` 名称。这些名称自 Python 3.10 起已弃用，但为了与 Python 2.5 及更低版本兼容，它们仍受支持。

> **CPython 实现细节：** 在 CPython 中，由于 [全局解释器锁]，一次只能有一个线程执行 Python 代码（尽管某些面向性能的库可能克服此限制）。如果你希望应用程序更好地利用多核机器的计算资源，建议使用 `multiprocessing` 或 `concurrent.futures.ProcessPoolExecutor`。但是，如果你想同时运行多个 I/O 密集型任务，线程仍然是一个合适的模型。

## GIL 和性能考虑

与使用独立进程绕过 [全局解释器锁]（GIL）的 `multiprocessing` 模块不同，`threading` 模块在单个进程内运行，这意味着所有线程共享同一内存空间。然而，GIL 限制了 `threading` 在 CPU 密集型任务方面的性能提升，因为一次只能有一个线程执行 Python 字节码。尽管如此，在许多场景下，线程仍然是实现并发的有用工具。

从 Python 3.13 开始，[自由线程] 构建可以禁用 GIL，从而实现线程的真正并行执行，但此功能默认不可用（参见 [PEP 703]）。


## Reference

### Thread 对象

`Thread` 类表示在单独的控制线程中运行的活动。有两种方式指定活动：向构造函数传递可调用对象，或在子类中重写 `run()` 方法。子类中不应重写其他方法（构造函数除外）。换句话说，只重写此类的 `__init__()` 和 `run()` 方法。

创建线程对象后，必须通过调用线程的 `start()` 方法来启动其活动。这会在单独的控制线程中调用 `run()` 方法。

线程活动启动后，该线程被视为“存活”。当它的 `run()` 方法终止时——无论是正常终止还是通过引发未处理异常终止——它就不再存活。`is_alive()` 方法测试线程是否存活。

其他线程可以调用线程的 `join()` 方法。这会阻塞调用线程，直到调用其 `join()` 方法的线程终止。

线程有一个名称。名称可以传递给构造函数，并通过 `name` 属性读取或更改。

如果 `run()` 方法引发异常，将调用 `threading.excepthook()` 来处理它。默认情况下，`threading.excepthook()` 会静默忽略 `SystemExit`。

线程可以被标记为“守护线程”。此标志的意义在于，当只剩下守护线程时，整个 Python 程序会退出。初始值从创建线程继承。可以通过 `daemon` 属性或 `daemon` 构造函数参数设置该标志。

> **备注**
> 守护线程在关闭时会突然停止。它们的资源（如打开的文件、数据库事务等）可能无法正确释放。如果你希望线程优雅地停止，请将它们设为非守护线程，并使用合适的信号机制，例如 `Event`。

有一个“主线程”对象；它对应于 Python 程序中的初始控制线程。它不是守护线程。

可能会创建“虚拟线程对象”。这些是对应于“外来线程”的线程对象，即从 `threading` 模块外部启动的控制线程，例如直接从 C 代码启动。虚拟线程对象的功能有限；它们始终被视为存活且为守护线程，并且不能被 `join`。它们永远不会被删除，因为无法检测外来线程的终止。

#### ♾️ `class threading.Thread` —— 构造尚未启动的线程对象

```python
class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, context=None)
```

> 常用来设置阻塞型函数到线程，并继续主程序控制流

此构造函数应始终使用关键字参数调用。参数包括：

- `group`  
  必须为 `None`，因为它保留给未来扩展，当实现 `ThreadGroup` 类时使用。

- `target`  
  是 `run()` 方法要调用的可调用对象。默认为 `None`，表示不调用任何内容。

- `name`  
  是线程名称。默认情况下，会构造一个唯一名称，形式为 `Thread-N`，其中 `N` 是一个小的十进制数；如果指定了 `target` 参数，则为 `Thread-N (target)`，其中 `target` 是 `target.__name__`。

- `args`  
  是目标调用的参数列表或元组。默认为 `()`。
  > 顺序的位置参数，(1, 2)

- `kwargs`  
  是目标调用的关键字参数字典。默认为 `{}`。
  > 指名参数，{"a": 1, "b": 2}

- `daemon`  
  如果不是 `None`，则显式设置线程是否为守护线程。如果为 `None`（默认值），则守护属性从当前线程继承。

- `context`  
  是启动线程时要使用的 `Context` 值。默认值为 `None`，表示由 `sys.flags.thread_inherit_context` 标志控制行为。如果标志为真，线程将以 `start()` 调用者上下文的副本启动。如果为假，它们将以空上下文启动。要显式以空上下文启动，请传入一个新的 `Context()` 实例。要显式以当前上下文的副本启动，请传入 `copy_context()` 的值。该标志在自由线程构建上默认为真，否则为假。

如果子类重写了构造函数，它必须确保在对线程执行任何其他操作之前调用基类构造函数（`Thread.__init__()`）。

在 3.3 版本发生变更：添加了 `daemon` 参数。

在 3.10 版本发生变更：如果省略 `name` 参数，则使用 `target` 名称。

在 3.14 版本发生变更：添加了 `context` 参数。

##### ♾️ `start` —— 启动新线程以执行线程对象设置的函数

```python
start()
```

启动线程的活动。

每个线程对象最多只能调用一次。它安排对象的 `run()` 方法在单独的控制线程中被调用。

> `start()` 创建新线程，并在其中调用 `run()` 执行线程对象

如果在同一个线程对象上调用多次，此方法将引发 [RuntimeError]。

如果支持，将操作系统线程名称设置为 `threading.Thread.name`。名称可能会根据操作系统线程名称限制而被截断。

在 3.14 版本发生变更：设置操作系统线程名称。

##### `run` —— 在当前线程调用函数

```python
run()
```

表示线程将被调用的的方法。

> 主线程中 `run()` 仅调用函数，无新线程创建

可以在子类中重写此方法。标准 `run()` 方法会调用传递给对象构造函数的可调用对象（作为 `target` 参数，如果有），并分别使用 `args` 和 `kwargs` 参数中的位置参数和关键字参数。

使用列表或元组作为传递给 `Thread` 的 `args` 参数可以实现相同的效果。

示例：

```python
>>> from threading import Thread
>>> t = Thread(target=print, args=[1])
>>> t.run()
1
>>> t = Thread(target=print, args=(1,))
>>> t.run()
1
```

##### ♾️ `join` —— 阻塞等待线程终止

```python
join(timeout=None)
```

等待直到线程终止。这会阻塞调用线程，直到调用其 `join()` 方法的线程终止——无论是正常终止还是通过未处理异常终止——或者直到发生可选的超时。

当 `timeout` 参数存在且不为 `None` 时，它应该是一个浮点数，指定操作的超时时间（以秒或秒的分数表示）。由于 `join()` 总是返回 `None`，你必须在 `join()` 之后调用 `is_alive()` 来决定是否发生了超时——如果线程仍然存活，则 `join()` 调用超时。

当 `timeout` 参数不存在或为 `None` 时，操作将阻塞直到线程终止。

一个线程可以被 join 多次。

`join()` 如果尝试 join 当前线程，会引发 [RuntimeError]，因为这会导致死锁。在线程启动之前 `join()` 它也是错误的，尝试这样做会引发相同的异常。

如果尝试在 Python 终结化的后期阶段 join 一个正在运行的守护线程，`join()` 会引发 [PythonFinalizationError]。

在 3.14 版本发生变更：可能引发 [PythonFinalizationError]。

##### `name`

仅用于标识目的的字符串。它没有语义。多个线程可以被赋予相同的名称。初始名称由构造函数设置。

在某些平台上，线程名称在线程启动时在操作系统级别设置，以便在任务管理器中可见。此名称可能会被截断以适应系统特定的限制（例如，Linux 上 15 字节或 macOS 上 63 字节）。

对 `name` 的更改仅在当前运行线程被重命名时才会反映在操作系统级别。（设置不同线程的 `name` 属性仅更新 Python `Thread` 对象。）

##### `getName` / `setName`

```python
getName()
setName()
```

已弃用的 `name` 的 getter/setter API；请直接将其用作属性。

自 3.10 版本弃用。

##### `ident`

此线程的“线程标识符”，如果线程尚未启动则为 `None`。这是一个非零整数。参见 `get_ident()` 函数。线程标识符在线程退出并创建另一个线程时可能会被回收。标识符在线程退出后仍然可用。

##### `native_id`

此线程的线程 ID（`TID`），由操作系统（内核）分配。这是一个非负整数，如果线程尚未启动则为 `None`。参见 `get_native_id()` 函数。此值可用于在系统范围内唯一标识此特定线程（直到线程终止，之后该值可能被操作系统回收）。

> **备注**
> 与进程 ID 类似，线程 ID 仅在从线程创建到线程终止期间有效（保证系统范围内唯一）。

可用性：Windows、FreeBSD、Linux、macOS、OpenBSD、NetBSD、AIX、DragonFlyBSD。

在 3.8 版本新增。

#### `is_alive`

```python
is_alive()
```

返回线程是否存活。

此方法在 `run()` 方法开始之前直到 `run()` 方法终止之后返回 `True`。模块函数 `enumerate()` 返回所有存活线程的列表。

##### `daemon`

一个布尔值，指示此线程是否为守护线程（`True`）或不是（`False`）。必须在调用 `start()` 之前设置，否则会引发 [RuntimeError]。其初始值从创建线程继承；主线程不是守护线程，因此主线程中创建的所有线程默认 `daemon = False`。

当没有存活的非守护线程时，整个 Python 程序退出。

##### `isDaemon` / `setDaemon`

```python
isDaemon()
setDaemon()
```

已弃用的 `daemon` 的 getter/setter API；请直接将其用作属性。

自 3.10 版本弃用。