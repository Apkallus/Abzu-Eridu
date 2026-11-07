# ctypes — Python 的外部函数库

https://docs.pythonlang.cn/3/library/ctypes.html


`ctypes` 是 Python 的一个外部函数库。它提供了与 C 兼容的数据类型，并允许调用 DLL 或共享库中的函数。它可用于用纯 Python 包装这些库。

> ctypes 提供对本地库和进程内存的低级访问，绕过了 Python 的安全机制并允许执行任意本地代码。

> SSTI 中可直接执行代码。但由于各种设置所需的赋值语句，导致无法读回
> 使用场景：`exec` 字符串代码执行 + `after_this_request` 设置返回钩子

```py
import ctypes

# 加载库
lib = ctypes.CDLL(None)

# 设置函数返回类型与参数类型
lib.popen.restype = ctypes.c_void_p
lib.fread.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_void_p]
lib.fread.restype = ctypes.c_size_t
lib.pclose.argtypes = [ctypes.c_void_p]

# 调用函数执行命令，将流存入缓冲区。
fp = lib.popen(b'ls -al', b'r')
buf = ctypes.create_string_buffer(4096)

# 读取缓冲区字符串
out_list = []
while (n := lib.fread(buf, 1, 4096, fp)) > 0:
    out_list.append(buf.raw[:n])

# 关闭指针并打印
lib.pclose(fp)
print(b''.join(out_list))
```


## ctypes 教程

### 基本数据类型

|ctypes 类型 | C 类型 | Python 类型 |
| --- | --- | --- |
|`c_char` | `char` | 1 字符 `bytes`|
|`c_wchar` | `wchar_t` | 1 字符 `str`|
|`c_size_t` | `size_t` | `int`|
|`c_char_p` | `char*`（以 `NUL` 结尾） | `bytes` 或 `None`|
|`c_wchar_p` | `wchar_t*`（以 `NUL` 结尾） | `str` 或 `None`|
|`c_void_p` | `void*` | `int` 或 `None`|

## ctypes 参考手册

### 加载共享库

将共享库加载到 Python 进程

#### class ctypes.CDLL()

```py
class ctypes.CDLL(name, mode=DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False, winmode=None)
```

此库中的函数使用标准的 C 调用约定，并假定返回 `int`
> 即，通常需显式设置函数的返回类型。例如，避免指针被截断

CPython 实现细节

由于 CPython 链接到了 `libc`，通常使用值为 `None` 的 `name` 来访问 C 标准库 
```py
printf = ctypes.CDLL(None).printf
```


### 外部函数

外部函数可以作为已加载共享库的属性来访问。

#### class ctypes._CFuncPtr

```py
class ctypes._CFuncPtr
```

外部函数的实例兼容 C 的数据类型，代表 C 函数指针。

对外部函数的参数赋值，以修改函数的返回类型、参数类型

- `restype`  
    分配一个 `ctypes` 类型来指定外部函数的结果类型。

- `argtypes`  
    分配一个 `ctypes` 类型的元组来指定函数接受的参数类型。

### 实用函数

#### ctypes.create_string_buffer()

```py
ctypes.create_string_buffer(init, size=None)
ctypes.create_string_buffer(size)
```

创建一个可变的字符缓冲区。返回的对象是 `c_char` 的 `ctypes` 数组。

属性
- `raw`  
    访问（或更改）当前的内存块内容

- `value`  
    作为以 `NUL` 结尾的字符串访问