# 内置类型

https://docs.python.org/zh-cn/3/builtins/stdtypes.html

以下章节描述了解释器内置的标准类型。

主要的内置类型是数值、序列、映射、类、实例和异常。

一些集合类是可变的。添加、删除或就地重新排列其成员的方法，以及不返回特定项的方法，永远不会返回集合实例本身，而是返回 `None`。

一些操作由多种对象类型支持；特别是，几乎所有的对象都可以进行相等性比较、真值测试，以及转换为字符串（使用 `repr()` 函数或稍有不同的 `str()` 函数）。当对象由 `print()` 函数写出时，会隐式使用后者。

## 真值测试

任何对象都可以进行真值测试，用于 `if` 或 `while` 条件，或作为下面布尔运算的操作数。

默认情况下，一个对象被认为是真，除非其类定义了返回 `False` 的 `__bool__()` 方法，或返回零的 `__len__()` 方法（当以该对象调用时）。[1] 如果其中一个方法在调用时引发异常，则异常会被传播，该对象没有真值（例如 `NotImplemented`）。以下是被视为假的大多数内置对象：

- 定义为假的常量：`None` 和 `False`
- 任何数值类型的零：`0`、`0.0`、`0j`、`Decimal(0)`、`Fraction(0, 1)`
- 空序列和集合：`''`、`()`、`[]`、`{}`、`set()`、`range(0)`

具有布尔结果的操作和内置函数总是对假返回 `0` 或 `False`，对真返回 `1` 或 `True`，除非另有说明。（重要的例外：布尔运算 `or` 和 `and` 总是返回其操作数之一。）

## 布尔运算 — `and`、`or`、`not`

以下是布尔运算，按优先级升序排列：

| 运算 | 结果 | 备注 |
| --- | --- | --- |
| `x or y` | 如果 *x* 为真，则为 *x*，否则为 *y* | (1) |
| `x and y` | 如果 *x* 为假，则为 *x*，否则为 *y* | (2) |
| `not x` | 如果 *x* 为假，则为 `True`，否则为 `False` | (3) |

备注：

1. 这是一个短路运算符，因此只有当第一个参数为假时才会对第二个参数求值。
2. 这是一个短路运算符，因此只有当第一个参数为真时才会对第二个参数求值。
3. `not` 的优先级低于非布尔运算符，因此 `not a == b` 被解释为 `not (a == b)`，而 `a == not b` 是语法错误。

## 文本序列类型 --- str

在 Python 中处理文本数据是使用 `str` 对象，也称为 字符串。字符串是由 Unicode 码位构成的不可变 [序列]。

字符串字面值有多种不同的写法：

```py
# 单引号
'允许包含有 "双" 引号'

# 双引号
"允许嵌入 '单' 引号"

# 三重引号
'''三重单引号''', """三重双引号"""
```

使用三重引号的字符串可以跨越多行 —— 其中所有的空白字符都将包含在该字符串字面值中。

### 字符串的方法

字符串实现了所有 [一般] 序列的操作，还额外提供了以下列出的一些附加方法。

#### string.replace() —— 子串替换

```py
string.replace(old, new[, count])
```  

返回字符串的副本，其中出现的所有子串 `old` 都将被替换为 `new`。

`count` 设置替换次数，默认全部替换

#### str.zfill() —— 补前导0

```py
str.zfill(width, /)
```

补前导`0`到 width。如果 `width` 小于等于 `len(s)` 则返回原字符串的副本。

```pycon
>>> "42".zfill(5)
'00042'
```

#### str.center() - 居中对齐

```py
str.center(width, fillchar=' ', /)
```

返回长度为 `width` 的居中字符串，使用指定的 `fillchar` 填充（默认为 ASCII 空格 ` `）。

```pycon
>>> 'Python'.center(10, '-')
'--Python--'
```

#### str.find() - 从左到右查找子串

```py
str.find(sub[, start[, end]])
```

在字符串的切片 `s[start:end]` 中，从左到右查找子串 `sub` 索引。未被找到则返回 `-1`

> 从右到左查找见 `str.rfind()`

#### str.rfind() - 从右到左查找子串

```py
str.rfind(sub[, start[, end]])
```

在字符串的切片 `s[start:end]` 中，从右到左查找子串 `sub` 索引。未被找到则返回 `-1`

> 从左到右查找见 `str.find()`

#### str.rsplit() - 从右到左拆分字符串

```py
str.rsplit(sep=None, maxsplit=-1)
```

从右到左，使用定界符 `sep` 拆分字符串；`maxsplit` 设置拆分次数，默认无限制。

> 从左到右见 `str.split()`

#### str.encode() - 编码字符串为 bytes

```py
str.encode(encoding='utf-8', errors='strict')
```

返回编码为 `bytes` 的字符串。

- `encoding` 默认为 `'utf-8'`；编码值详见 [标准编码]。
    > 常用 ASCII 的 `latin-1`（简写为 `l1`）

## 数字类型 - int, float, complex

存在三种不同的数字类型：`整数`, `浮点数` 和 `复数`。此外，布尔值属于整数的子类型。整数具有无限的精度。 浮点数通常使用 C 中的 `double` 来实现

### 整数类型的附加方法

#### int.bit_count()

```py
int.bit_count()
```

返回整数的绝对值的二进制表示中 1 的个数

#### int.to_bytes() —— 将数字转为字节串

```py
int.to_bytes(length=1, byteorder='big', *, signed=False)
```

将数字转为字节串，设置长度、大小端序、符号（也可用 `struct` 包）

```pycon
>>> (1024).to_bytes(2, byteorder='big')
b'\x04\x00'
```

- `length`  
    字节串的长度。如果整数不能用给定的字节数来表示则会引发 `OverflowError`。

- `byteorder`  
    字节序
    - `"big"` 最高位字节将放在字节数组的开头
    - `"little"` 最高位字节将放在字节数组的末尾

- `signed`  
    补码表示法开关。
    - `False` 不使用补码形式，若为负整数则引发 `OverflowError`
    - `True` 设置正负补码形式

#### classmethod int.from_bytes()

```py
classmethod 
int.from_bytes(bytes, byteorder='big', *, signed=False)
```

将字节串传为整数

```pycon
>>> int.from_bytes(b'\x00\x10', byteorder='big')
16
```

- `bytes`  
    一个 `bytes-like object` 或是生成字节的可迭代对象。
- `byteorder`  
    表示整数的字节顺序
- `signed`  
    补码表示法开关。
    
## Binary Sequence Types —— bytes, bytearray, memoryview

用于操作二进制数据的核心内置类型是 `[bytes]` 和 `[bytearray]`。它们由 `[memoryview]` 支持，后者使用 `[缓冲区协议]` 访问其他二进制对象的内存，而无需进行复制。

`[array]` 模块支持高效存储基本数据类型，例如 32 位整数和 IEEE754 双精度浮点值。

### bytes 对象

`[bytes]` 对象是单个字节的不可变序列。由于许多主流二进制协议基于 ASCII 文本编码，字节对象提供了若干仅在处理 ASCII 兼容数据时有效的方法，并在其他多方面与字符串对象密切相关。

#### class bytes()

```python
class bytes(source=b'')
class bytes(source, encoding, errors='strict')
```

首先，字节字面量的语法与字符串字面量大致相同，只是添加了 `b` 前缀：

```python
# 单引号
b'still allows embedded "double" quotes'

# 双引号
b"still allows embedded 'single' quotes"

# 三引号
b'''3 single quotes'''
b"""3 double quotes"""
```

字节字面量中只允许 ASCII 字符（无论声明的源代码编码是什么）。任何大于 127 的二进制值都必须使用适当的转义序列输入到字节字面量中。

与字符串字面量一样，字节字面量也可以使用 `r` 前缀来禁用转义序列处理。有关各种形式的字节字面量（包括支持的转义序列）的更多信息，请参见 `[字符串和字节字面量]`。

虽然字节字面量和表示基于 ASCII 文本，但字节对象实际上表现得像不可变的整数序列，序列中的每个值都被限制为 `0 <= x < 256`（试图违反此限制将触发 `[ValueError]`）。这样做是故意的，以强调虽然许多二进制格式包含基于 ASCII 的元素，并且可以有效地使用一些面向文本的算法进行操作，但任意二进制数据通常并非如此（盲目地将文本处理算法应用于非 ASCII 兼容的二进制数据格式通常会导致数据损坏）。

除了字面量形式外，还可以通过多种其他方式创建字节对象：

```python
# 指定长度的零填充字节对象
bytes(10)

# 从整数可迭代对象
bytes(range(20))

# 通过缓冲区协议复制现有二进制数据
bytes(obj)
```

另请参见内置的 `[bytes]`。

由于 2 个十六进制数字恰好对应一个字节，十六进制数字是描述二进制数据的常用格式。因此，`bytes` 类型有一个额外的类方法来读取该格式的数据：

##### classmethod fromhex()

```python
classmethod fromhex(string, /)
```

`bytes` 类方法，输入字符串、ASCII `bytes` 或 [字节型对象]，返回转换后的 `bytes` 对象。该字符串必须每字节包含两个十六进制数字，ASCII 空白字符将被忽略。

```python
>>> bytes.fromhex('2Ef0 F1f2  ')
b'.\xf0\xf1\xf2'
```

存在一个反向转换函数 `hex()`，用于将 `bytes` 对象转换为其十六进制字符串表示形式。

##### hex()

```python
hex(*, bytes_per_sep=1)
hex(sep, bytes_per_sep=1)
```

返回一个字符串对象，其中包含实例中每个字节的两个十六进制数字。

```python
>>> b'\xf0\xf1\xf2'.hex()
'f0f1f2'
```

参数
- `sep`  
  字符分隔符，即字符之间的分隔符，默认为空。

- `bytes_per_sep`  
  控制字符分隔符的间隔，默认为1。正值从右侧计算分隔符位置，负值从左侧计算。

```python
>>> value = b'\xf0\xf1\xf2'
>>> value.hex('-')
'f0-f1-f2'
>>> value.hex('_', 2)
'f0_f1f2'
>>> b'UUDDLRLRAB'.hex(' ', -4)
'55554444 4c524c52 4142'
```

由于 bytes 对象是整数序列（类似于元组），对于 bytes 对象 `b`，`b[0]` 将是整数，而 `b[0:1]` 将是长度为 1 的 bytes 对象。（这与文本字符串相反，文本字符串的索引和切片都会产生长度为 1 的字符串。）
> 经常造成类型转换错误：尝试使用索引获得字节导致异常

bytes 对象的表示使用字面量格式（`b'...'` 即字节串）。使用 `list(b)` 将 bytes 对象转换为整数列表


## 映射类型 --- dict，frozendict

### class dict()

```py
class dict(**kwargs)
class dict(mapping, /, **kwargs)
class dict(iterable, /, **kwargs)
```

返回一个新的字典，基于可选的位置参数和可能为空的关键字参数集来初始化。

#### setdefault()

```py
setdefault(key, default=None, /)
```

如果字典存在键 `key` ，返回它的值。如果不存在，插入值为 `default` 的键 `key` ，并返回 `default` 