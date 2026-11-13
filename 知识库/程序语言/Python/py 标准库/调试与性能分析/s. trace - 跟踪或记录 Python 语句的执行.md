https://docs.python.org/zh-cn/3/library/trace.html

# trace --- 跟踪或记录 Python 语句的执行

`trace` 模块允许你跟踪程序执行，生成带注解的语句覆盖率列表，打印调用者/被调用者关系以及列出程序运行过程中执行的函数。 它可以在其他程序中使用或从命令行使用。

## 命令行用法

trace 模块可以从命令行调用。 只需简单地

```sh
python -m trace --count -C . somefile.py ...
```

上述命令将执行 `somefile.py` ，并在当前目录生成执行期间所有已导入 Python 模块的带注解列表。