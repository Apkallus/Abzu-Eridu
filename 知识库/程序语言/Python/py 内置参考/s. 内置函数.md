https://docs.python.org/zh-cn/3/library/functions.html

# 内置函数

## bin() —— 整数转二进制字符串

```py
bin(integer, /)
```

将整数转换为以 `0b` 开头的二进制字符串。

```pycon
>>> bin(3)
'0b11'
```

## hex() —— 整数转十六进制字符串

```py
hex(integer, /)
```

将整数转换为以 `0x` 开头的十六进制小写字符串。

```pycon
>>> hex(255)
'0xff'
```

## class str()

```py
class str(*, encoding='utf-8', errors='strict')
class str(object)
class str(object, encoding, errors='strict')
class str(object, *, errors)
```

返回一个 `str` 版本的 `object` 。

```pycon
>>> str(0)
'0'
```

## format() 格式化

```py
format(value, format_spec='', /)
```

将值转换为由 `format_spec` 控制的“格式化”表示形式。`format_spec` 的解释取决于 `value` 参数的类型；不过，大多数内置类型都使用一种标准的格式化语法：[格式规范迷你语言]。

默认的 `format_spec` 为空字符串，其效果通常与调用 `[str(value)]` 相同。

对 `format(value, format_spec)` 的调用会被转换为 `type(value).__format__(value, format_spec)`，这在查找值的 `[__format__()]` 方法时会绕过实例字典。

如果方法查找到达 `[object]` 且 `format_spec` 非空，或者 `format_spec` 或返回值不是字符串，则会引发 `[TypeError]` 异常。

在 3.4 版本发生变更：如果 `format_spec` 不是空字符串，`object().__format__(format_spec)` 会引发 `[TypeError]`。


示例

```py
# 设置模板字符串
template = 'Host: {target_host}'
# 填充模板字符串
template.format(target_host="localhost")
```

## `ord(c)` —— 转字符为 Unicode 码

对表示单个 Unicode 字符的字符串，返回代表它 Unicode 码点的整数。这是 `chr()` 的逆函数。

例如 
```py
ord('a') # 整数 97
ord('€') # 返回 8364 
```

## class int() —— 转为选定进制的 int 对象

```py
class int(x, base=10)
```

返回一个基于数字或字符串 `x` 构造的整数对象，或者在未给出参数时返回 0。 

默认的 `base` 为 10。 允许的基数为 0 和 2--36。 对于基数 2, -8 和 -16 来说字符串前面还能加上可选的 `0b/0B`, `0o/0O` 或 `0x/0X` 前缀，就像代码中的整数字面值那样。 

```pycon
# 二进制字符串转 int
>>> int('10100111001', 2)
1337

# 拥有 `0x` 前缀的十六进制字符串转 int
>>> int('0x539', 16)
1337

# `0` 填充前缀的十六进制数字
>>> int('00000539', 16)
1337
```

## all() —— 批量布尔运算

```py
all(iterable, /)
```

如果 `iterable` 的所有元素均为真值（或可迭代对象为空）则返回 `True`。等价于:

```py
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```

## iter() - 返回一个迭代器

```py
iter(iterable, /)
iter(callable, sentinel, /)
```

返回一个 `iterator` 对象。
- 若没有提供第二个参数，则该单一参数必须是一个支持 `iterable` 协议（即实现了 `__iter__()` 方法）的多项集对象，或者必须支持序列协议（即实现了以从 0 开始的整数参数调用的 `__getitem__()` 方法）。
- 如果提供了第二个参数 `sentinel`，则第一个参数必须是一个可调用对象。 在这种情况下创建的迭代器会在每次调用其 `__next__()` 方法时，无参数地调用该*可调用对象*

## next()

```py
next(iterator, /)
next(iterator, default, /)
```

通过调用 `iterator` 的 `__next__()` 方法获取下一个元素。如果迭代器耗尽，则返回给定的 `default`，如果没有默认值则触发 `StopIteration。`

## chr()

```py
chr(codepoint, /)
```

返回表示具有指定 Unicode 码点的字符的字符串。例如，`chr(97)` 返回字符串 `'a'`，而 `chr(8364)` 返回字符串 `'€'`。这是 `[ord()]` 的逆操作。

参数的有效范围是从 0 到 1,114,111（十六进制的 `0x10FFFF`）。如果超出该范围，将引发 `[ValueError]`。

## open()

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

打开 `file` 并返回相应的[文件对象]。如果文件无法打开，则引发 `OSError`。有关如何使用此函数的更多示例，请参见[读写文件]。

`file` 是[类路径对象]，给出要打开文件的路径名（绝对路径或相对于当前工作目录的路径），或要包装的文件的整数文件描述符。（如果给出文件描述符，则当返回的 I/O 对象关闭时，该文件描述符会关闭，除非 `closefd` 设置为 `False`。）

`mode` 是可选字符串，指定打开文件的模式。在文本模式下，如果未指定 `encoding`，默认使用 UTF-8。可用模式如下：

- `'r'`：打开读取（默认）
- `'w'`：打开写入，先截断文件
- `'x'`：打开独占创建，如果文件已存在则失败
- `'a'`：打开写入，如果文件存在则追加到文件末尾
- `'b'`：二进制模式
- `'t'`：文本模式（默认）
- `'+'`：打开更新（读取和写入）

默认模式是 `'r'`（打开读取文本，是 `'rt'` 的同义词）。模式 `'w+'` 和 `'w+b'` 会打开并截断文件。模式 `'r+'` 和 `'r+b'` 打开文件时不截断。

如[概述]中所述，Python 区分二进制 I/O 和文本 I/O。以二进制模式打开的文件（包括 `mode` 参数中包含 `'b'`）返回 `bytes` 对象作为内容，不进行任何解码。在文本模式（默认，或 `mode` 参数中包含 `'t'`）下，文件内容作为 `str` 返回，字节首先使用默认编码解码，或在指定 `encoding` 时使用指定编码解码。

> **备注**
>
> Python 不依赖底层操作系统的文本文件概念；所有处理都由 Python 本身完成，因此与平台无关。

`buffering` 是可选整数，用于设置缓冲策略。传递 0 以关闭缓冲（仅允许在二进制模式下），传递 1 以选择行缓冲（仅在文本模式下写入时可用），传递大于 1 的整数以指示固定大小块缓冲区的字节大小

`encoding` 是用于解码或编码文件的编码名称。只应在文本模式下使用。默认编码是 UTF-8

`newline` 决定如何从流中解析换行字符。它可以是 `None`（通用换行模式）、`''`、`'\n'`、`'\r'` 和 `'\r\n'`。

以下示例使用 `os.open()` 函数的 [dir_fd] 参数打开相对于给定目录的文件：

```py
>>> import os
>>> dir_fd = os.open('somedir', os.O_RDONLY)
>>> def opener(path, flags):
...     return os.open(path, flags, dir_fd=dir_fd)
...
>>> with open('spamspam.txt', 'w', opener=opener) as f:
...     print('This will be written to somedir/spamspam.txt', file=f)
...
>>> os.close(dir_fd)  # 不要泄漏文件描述符
```

`open()` 函数返回的[文件对象]类型取决于模式。

##  `__import__()`

```py
__import__(name, globals=None, locals=None, fromlist=(), level=0)
```

> 常用于构造链式载荷

此函数由 `import` 语句唤起。可通过 `builtins.__import__` 访问

```py
# 自定义函数
def foo():
    pass

print(
    # 位于 __main__ 时：访问全局字典 -> builtins 模块（非 __main__ 时为字典） -> 属性
    foo.__globals__["__builtins__"].__import__("subprocess").getoutput("id"),
    # 访问 builtins 字典 -> 条目
    foo.__builtins__["__import__"]("subprocess").getoutput("id"),
    sep='\n'
)
```

## isinstance()

```py
isinstance(object, classinfo, /)
```

- 如果 `object` 参数是 `classinfo` 参数的实例，或者是其 (直接、间接或 虚拟) 子类的实例则返回 `True`。
- 如果 `object` 不是给定类型的对象，则该函数总是返回 `False`。
- 如果 `classinfo` 是由类型对象结成的元组 (或是由其他此类元组递归生成) 或者是多个类型的 `union` 类型，则如果 `object` 是其中任一类型的实例时将会返回 `True`。
- 如果 `classinfo` 不是一个类型或类型元组及此类元组，则会引发 `TypeError` 异常。
- 如果之前的检查成功执行则可能不会为无效的类型引发 `TypeError`


## round()

```py
round(number, ndigits=None)
```

返回 `number` 舍入到小数点后 `ndigits` 位精度的值。如果 `ndigits` 被省略或为 `None`，则返回最接近输入值的整数。