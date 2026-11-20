https://docs.python.org/zh-cn/3/builtins/exceptions.html

# 内置异常

在 Python 中，所有异常必须为一个派生自 `BaseException` 的类的实例。

## 具体异常

以下异常属于经常被引发的异常。

### exception KeyboardInterrupt - 键盘中断

```py
exception KeyboardInterrupt
```

当用户按下中断键 (通常为 `Control-C` 或 `Delete`) 时将被引发。

### exception RuntimeError - 广泛的异常

```py
exception RuntimeError
```

当检测到一个不归属于任何其他类别的错误时将被引发。关联的值是一个指明究竟发生了什么问题的字符串。

### exception ValueError - 值错误

当操作或函数接收到具有正确类型但值不适合的参数，并且情况不能用更精确的异常例如 `IndexError` 来描述时将被引发。

### exception NotImplementedError - 未实现

此异常派生自 `RuntimeError`。 在用户自定义的基类中，抽象方法应当在其要求所派生类重写该方法，或是在其要求所开发的类提示具体实现尚待添加时引发此异常。