https://docs.python.org/zh-cn/3/library/signal.html

# signal --- 设置异步事件处理器¶

该模块提供了在 Python 中使用信号处理程序的机制。

## 一般规则

`signal.signal()` 函数允许定义在接收到信号时执行的自定义处理程序。

## 模块内容

### signal.SIGTERM

终结信号。

### signal.SIGHUP

在控制终端上检测到挂起或控制进程的终止。

### signal.SIGINT

来自键盘的中断 (CTRL + C)。

默认的动作是引发 `KeyboardInterrupt`。

### signal.signal()

```py
signal.signal(signalnum, handler)
```

将信号 `signalnum` 的处理程序设为函数 `handler`。 

### signal.SIGWINCH

窗口调整大小信号。

可用性: Unix.


## 例子

```py
import signal, os

def handler(signum, frame):
    signame = signal.Signals(signum).name
    print(f'Signal handler called with signal {signame} ({signum})')
    raise OSError("Couldn't open device!")

# 设置信号处理器及 5 秒警报
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# open() 可能会无限挂起
fd = os.open('/dev/ttyS0', os.O_RDWR)

signal.alarm(0)          # 禁用警报
```


