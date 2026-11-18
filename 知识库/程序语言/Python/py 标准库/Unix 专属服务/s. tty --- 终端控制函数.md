https://docs.python.org/zh-cn/3/library/tty.html

# tty --- 终端控制函数

`tty` 模块定义了将 `tty` 设为 `cbreak` 和 `raw` 模式的函数。

可用性: Unix.

因为它需要 `termios` 模块，所以只能在 Unix 上运行。

## tty.setcbreak()

```py
tty.setcbreak(fd, when=termios.TCSAFLUSH)
```

将文件描述符 `fd` 的模式改为 `cbreak`。 如果 when 被省略，它将默认为 `termios.TCSAFLUSH`，并将被传给 `termios.tcsetattr()`。 `termios.tcgetattr()` 的返回值在将 `fd` 设为 `cbreak` 模式前会被保存；该值将被返回。

这将清除 `ECHO` 和 `ICANON` 本地模式旗标并将最小输入设为 1 字节且无延迟。

> 返回值为终端状态，后续使用 `termios.tcsetattr()` 恢复