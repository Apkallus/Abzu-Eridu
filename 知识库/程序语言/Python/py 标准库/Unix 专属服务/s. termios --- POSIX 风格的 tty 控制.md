https://docs.python.org/zh-cn/3/library/termios.html

# termios --- POSIX 风格的 tty 控制

此模块提供了针对 tty I/O 控制的 POSIX 调用的接口。有关此类调用的完整描述，请参阅 [termios(3)](https://manpages.debian.org/trixie/manpages-dev/termios.3.en.html) Unix 指南页。

## termios.tcgetattr()

```py
termios.tcgetattr(fd)
```

返回一个包含文件描述符 `fd` 的 `tty` 属性的列表

##  termios.tcsetattr()

```py
termios.tcsetattr(fd, when, attributes)
```

根据 `attributes` 为文件描述符 `fd` 设置 `tty` 的属性，它是一个类似于 `tcgetattr()` 的返回值的列表。 `when` 参数决定这些属性在何时被更改：

- `termios.TCSANOW`  
    立即更改属性。
