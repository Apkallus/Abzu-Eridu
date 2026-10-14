# subprocess 子进程管理

https://docs.python.org/zh-cn/3.15/library/subprocess.html

subprocess 模块允许你生成新的进程，连接它们的输入、输出、错误管道，并且获取它们的返回码。

## 使用 subprocess 模块

推荐的调用子进程的方式是在任何它支持的用例中使用 [`run()`] 函数。对于更进阶的用例，也可以使用底层的 [`Popen`] 接口。

例如：
```py

p = subprocess.run(
    ["/challenge/目标程序"], # 要执行的命令（列表形式），
    input=payload,          # 作为 stdin 发送的内容（bytes）
    capture_output=True,     # 捕获 stdout 和 stderr
    text=False               # False 表示 input 为 bytes，否则为 str
    )

if b"pwn.college" in p.stdout:
    print(f"response: {p.stdout}")
```

#### `subprocess.run()` —— 运行指令

```py
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None, **other_popen_kwargs)
```

运行被 `args` 描述的指令。等待指令完成，然后返回一个 [`CompletedProcess`] 实例。

如果 `capture_output` 为真值，则 `stdout` 和 `stderr` 将被捕获。
> 注意 `capture_output=False` 默认不捕获输出

`text` 文本型开关。（默认为字节型）

```py
# 列表型参数
subprocess.run(["ls", "-l"])  # 不捕获输出
"""CompletedProcess(args=['ls', '-l'], returncode=0)"""

# shell 型字符串参数
subprocess.run("exit 1", shell=True, check=True)
"""Traceback (most recent call last):
  ...
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1"""

subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
"""CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')"""
```

对应反序列化的两种格式
```py
# 列表型参数
obj_list = subprocess.run
argvs_list = (["ls", "-al"], )
type_list = (obj_list, argvs_list)

# shell 型字符串参数，使用 `functools.partial` 部分固定命名参数
obj_shell = functools.partial(subprocess.run, shell=True)
argvs_shell = (["ls -al"], True)
type_shell = (obj_shell, argvs_shell)
```

#### class subprocess.CompletedProcess

[`run()`] 的返回值，代表一个进程已经结束。

- `args`
    被用作启动进程的参数。可能是一个列表或字符串。

- `returncode`
    子进程的退出状态码。通常来说，一个为 0 的退出码表示进程运行正常。

    一个负值 `-N` 表示子进程被信号 `N` 中断 (仅 POSIX).

- `stdout`
    从子进程捕获到的标准输出。 一个字节序列，或者如果 `run()` 是设置了 `encoding`, `errors` 或者 `text=True` 来运行的则为一个字符串。 如果标准输出未被捕获则该值为 `None`。

    如果你通过 `stderr=subprocess.STDOUT` 运行进程，标准输出和标准错误将被组合在这个属性中，并且 `stderr` 将为 `None`。

- `stderr`
    捕获到的子进程的标准错误。 一个字节序列，或者如果 `run()` 是设置了参数 `encoding`, `errors` 或者 `text=True` 运行的则为一个字符串。 如果标准错误未被捕获则该值为 `None`。

- `check_returncode()`
    如果 [`returncode`] 非零，则会抛出 [`CalledProcessError`] 异常。


### Popen 构造函数

此模块的底层的进程创建与管理由 [`Popen`] 类处理。它提供了很大的灵活性，因此开发者能够处理未被便利函数覆盖的不常见用例。

```py
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, group=None, extra_groups=None, user=None, umask=-1, encoding=None, errors=None, text=None, pipesize=-1, process_group=None)
```

在一个新的进程中执行子程序。在 POSIX 上，该类会使用类似于 [`os.execvpe()`] 的行为来执行子程序。在 Windows 上，该类会使用 `Windows CreateProcess()` 函数。 

## 较旧的高阶 API

```py
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=None, timeout=None, text=None, **other_popen_kwargs)
```
- 附带参数运行命令并返回其输出。

## 使用 subprocess 模块替代旧有函数

https://docs.python.org/zh-cn/3.15/library/subprocess.html#replacing-older-functions-with-the-subprocess-module