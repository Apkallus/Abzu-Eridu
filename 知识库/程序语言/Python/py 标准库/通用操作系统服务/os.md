# os

https://docs.python.org/3.14/library/os.html

- ```os.walk()``` 
    递归遍历目录
    ```python
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
    ```
    ```Iterator[tuple[AnyStr@walk, list[AnyStr@walk], list[AnyStr@walk]]]```
    迭代器返回的三元组均为字符串或字符串列表，搭配 ```os.path.join()``` 拼接路径

- `os.path.join('路径1','路径2','路径N')`
    拼接路径  
    在非空参数间添加路径分隔符号。  
    路径可为目录或文件名，可为仅最后一个生效的绝对路径

- `os.path.relpath(path, startPath)`
    计算基于起始路径的相对路径

- `os.path.dirname(path)`
    返回路径名 path 的目录名

- `os.path.abspath(path)`
    返回路径名 path 的规范化绝对化版本。

- `os.urandom(n)`
    随机字节生成。  
    `secrets.token_bytes(n)` 为对应的安全封装函数

- `os.symlink(src, dst)`
    创建符号链接

- `os.remove(path)`
    删除指定路径的文件。如果指定的路径是一个目录，将抛出OSError。

- `os.rename("old_name.txt", "new_name.txt")`
    重命名文件或目录。src 是原始路径，dst 是新的路径。

- `os.mkdir(path[, mode])`
    以数字权限模式创建目录（单级目录）

- `os.makedirs()`
    创建多级目录，并可设置 `exist_ok=True` 以忽略目录已存在的报错

- `os.open(path, flags, mode=0o777, *, dir_fd=None)`
    打开文件 path，根据 flags 设置各种标志位，并根据 mode 设置其权限状态。当计算 mode 时，会首先根据当前 umask 值将部分权限去除。本方法返回新文件的描述符。新的文件描述符是 不可继承 的。
    - 例 `os.open("example.txt", os.O_RDWR)`



- `os.pread(fd, n, offset, /)`
    从文件描述符 `fd` 的偏移位置 `offset` 处最多读取 `n` 个字节，且不改变文件偏移量。
    返回包含读取字节的字节串。如果已到达 `fd` 所指向文件的末尾，则返回空字节对象。

- `os.pwrite(fd, str, offset, /)`
    将 str 中的字节串 (bytestring) 写入文件描述符 fd 的偏移位置 offset 处，保持文件偏移量不变。
    
- `os.truncate(path, length)`
    截断 path 对应的文件，以使其最大为 length 字节。
    本函数支持 指定文件描述符为参数。

- `os.dup(fd)`
    得到 fd 的副本

- `os.set_inheritable(fd, inheritable)`
    设置指定文件描述符的“可继承”标志位（为布尔值）。

    文件描述符的继承:
    每个文件描述符都有一个 "inheritable"（可继承）标志位，该标志位控制了文件描述符是否可以由子进程继承。从 Python 3.4 开始，由 Python 创建的文件描述符**默认是不可继承的**。

- `os.fork()` 
    创建子进程

    ```py

    print("before fork")
    pid = os.fork()

    if pid == 0:
        print("child in")
        # child

        pass

        print("child out")
        os._exit(0)

    elif pid > 0:
        print("parent in")
        # parent

            pass

        print("parent out, start wait")
        os.waitpid(pid, 0) # 或子进程持续运行，直到父进程使用 os.kill(pid, 9)
        print("parent wait end")
    ```
- `os.wait()`
    等待子进程的完成

- `os._exit(n)`
    以状态码 `n` **退出进程**，不调用清理处理程序，也不刷新 stdio 缓冲区等。

    **注意** 退出的标准方式是 `sys.exit(n)`。`_exit()` 通常只应在 `fork()` 之后的子进程中使用。

    以下退出代码已被定义，可与 `_exit()` 一起使用（尽管并非必须）。这些退出代码通常用于用 Python 编写的系统程序，例如邮件服务器的外部命令投递程序。

- `os.environ` 查看环境变量
    - `os.environ['SUDO_USER']`

## 文件描述符操作

### os.lseek

```py
os.lseek(fd, pos, whence, /)
```
> 对应 python 内置 `open` 函数打开的文件对象中的 `f.seek()`

将文件描述符 `fd` 的当前位置设置为由 `whence` 调整后的位置 `pos`，并返回相对于文件开头的新位置（以字节为单位）。`whence` 的有效取值包括：

- `SEEK_SET` 或 `0` – 相对于文件开头设置 `pos`
- `SEEK_CUR` 或 `1` – 相对于当前文件位置设置 `pos`
- `SEEK_END` 或 `2` – 相对于文件末尾设置 `pos`
- `SEEK_HOLE` – 将 `pos` 设置为相对于 `pos` 的下一个数据空洞位置
- `SEEK_DATA` – 将 `pos` 设置为相对于 `pos` 的下一个数据位置

## 进程管理

下列函数可用于创建和管理进程。

所有 [`exec*`] 函数都接受一个参数列表，用来给新程序加载到它的进程中。在所有情况下，传递给新程序的第一个参数是程序本身的名称，而不是用户在命令行上输入的参数。对于 C 程序员来说，这就是传递给 `main()` 函数的 `argv[0]`。例如，`os.execv('/bin/echo', ['foo', 'bar'])` 只会在标准输出上打印 `bar`，而 `foo` 会被忽略。


### os.popen() —— 打开一个通往或接受命令 `cmd` 的管道 —— 已废弃

```py
os.popen(cmd, mode='r', buffering=-1)
```

打开一个通往或接受命令 `cmd` 的管道。

> `popen()` 是针对 [`subprocess.Popen`] 的简单包装器。使用 `subprocess.Popen` 或 `subprocess.run()` 来控制编码格式等选项。