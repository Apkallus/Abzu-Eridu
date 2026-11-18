https://docs.python.org/zh-cn/3/builtins/exceptions.html

# 内置异常

在 Python 中，所有异常必须为一个派生自 `BaseException` 的类的实例。

## 具体异常

以下异常属于经常被引发的异常。

### exception KeyboardInterrupt

```py
exception KeyboardInterrupt
```

当用户按下中断键 (通常为 `Control-C` 或 `Delete`) 时将被引发。

### exception RuntimeError

```py
exception RuntimeError
```

当检测到一个不归属于任何其他类别的错误时将被引发。关联的值是一个指明究竟发生了什么问题的字符串。


### exception ValueError

当操作或函数接收到具有正确类型但值不适合的参数，并且情况不能用更精确的异常例如 `IndexError` 来描述时将被引发。