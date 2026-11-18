https://docs.python.org/zh-cn/3/library/select.html

# select --- 等待 I/O 完成

该模块提供了对 `select()` 和 `poll()` 函数的访问，这在大多数操作系统上都是可用的。

```py
# 读取标准输入，直到输入退出键 `q` 
def getch():
    key = None
    if select.select([STDIN_FD], [], [], 0)[0]:
        # 得到 bytes
        key = os.read(STDIN_FD, 32)
    return key

while True:
    key = getch()
    # 若收到键盘 `q` 则退出
    if key and QUIT_KEY in key:
        break
```

```py
# 注册轮询对象，等待数据读取
POLL_OBJ = select.poll()
POLL_OBJ.register(STDIN_FD, select.POLLIN)
# 休眠时间，同时等待数据读取事件。根据返回列表是否为空得到事件 flag
key_flag = bool(POLL_OBJ.poll(time_sleep_s * 1000))
# 若存在数据读取事件，则读取
if key_flag:
    key = os.read(STDIN_FD, 32)
```

### select.select()

```py
select.select(rlist, wlist, xlist, timeout=None)
```

Unix `select()` 系统调用接口。输入文件描述符列表

- `rlist`   
    等待，直到可以开始读取

- `wlist`  
    等待，直到可以开始写入

- `xlist`  
    等待“异常情况”（请参阅当前系统的手册，以获取哪些情况称为异常情况）

- `timeout`  
    默认阻塞轮询，为零则永不阻塞

返回值是三个列表，包含已就绪对象，返回的三个列表是前三个参数的子集。当超时时间已到且没有文件描述符就绪时，返回三个空列表。

### select.poll()

```py
select.poll()
```

返回一个轮询对象，它支持注册和注销文件描述符，然后轮询它们以获取 I/O 事件；请参阅下面的 轮询对象 一节了解轮询对象支持的方法。

可用性: Unix.

## 轮询对象

`poll()` 的可伸缩性更好是因为该系统只须列出要关注的文件描述符，而 `select()` 则会构建一个位映射表，打开这个要关注的描述符所对应的比特位，然后再次线性扫描整个位映射表。 `select()` 的复杂度为 O(最高文件描述符)，而 `poll()` 则为 O(文件描述符的数量)。

### poll.register()

```py
poll.register(fd[, eventmask])
```

在轮询对象中注册文件描述符。这样，将来调用 `poll()` 方法时将检查文件描述符是否有未处理的 I/O 事件。`fd` 可以是整数，也可以是带有 `fileno()` 方法的对象（该方法返回一个整数）。文件对象已经实现了 `fileno()`，因此它们也可以用作参数。

`eventmask` 是可选的位掩码，用于指定要检查的事件类型

- `POLLIN`  
	有数据可读。

### poll.poll()

```py
poll.poll([timeout])
```

轮询已注册的文件描述符的集合，并返回一个列表，列表可能为空，也可能有多个 `(fd, event)` 2 元组，其中包含了要报告事件或错误的描述符。 

- `fd` 是文件描述符
- `event` 是一个位掩码，表示该描述符所报告的事件 --- `POLLIN` 表示等待输入，`POLLOUT` 表示该描述符可以写入，依此类推。

空列表表示调用超时，没有任何文件描述符报告事件。如果指定了 `timeout`，它将指定系统等待事件时，等待多长时间后返回（以毫秒为单位）。如果 `timeout` 被省略、为负数或为 `None`，则本调用将阻塞，直到轮询对象发生事件为止。

