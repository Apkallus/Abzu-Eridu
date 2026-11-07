https://docs.python.org/zh-cn/3/library/sys.html

# sys --- 系统相关的形参和函数

该模块提供了一些由解释器使用或维护的变量以及与解释器高强度交互的函数。除非显式地说明例外情况，所有变量都是只读的。

## sys.argv

一个列表，其中包含了被传递给 Python 脚本的命令行参数。`argv[0]` 为脚本的名称（是否是完整的路径名取决于操作系统）。

## sys.byteorder

本地字节顺序的指示符。在大端序（最高有效位优先）操作系统上值为 `'big'`，在小端序（最低有效位优先）操作系统上为 `'little'` 。

## sys.stdin, sys.stdout, sys.stderr

解释器用于标准输入、标准输出和标准错误的 [文件对象]:

这些流都是常规 [文本文件]，与 `open()` 函数返回的对象一致。

要从标准流写入或读取二进制数据，使用底层二进制 [buffer] 对象。例如，要将字节写入 `stdout`，使用：

```py
sys.stdout.buffer.write(b'abc')
```

## sys.exit()

```py
sys.exit([arg])
```

引发一个 `SystemExit` 异常，表示打算退出解释器。

- `arg`  
    可为一个表示退出状态的整数（默认为零），或为其他类型的对象