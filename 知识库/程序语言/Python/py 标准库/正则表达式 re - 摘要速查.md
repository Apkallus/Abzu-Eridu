# re - 正则表达式操作

https://docs.python.org/zh-cn/3.14/library/re.html

模式和被搜索的字符串既可以是 Unicode 字符串 `str`，也可以是 8 位字节串 `bytes`，但需使用相同类型。

正则表达式使用反斜杠字符 `'\'` 表示特殊形式或是允许在使用特殊字符时不引发它们的特殊含义。对于正则表达式模式使用 Python 的原始字符串表示法；在带有 `r` 前缀的字符串字面值中，反斜杠不必做任何特殊处理。因此 `r"\n"` 表示包含 `'\'` 和 `'n'` 两个字符的字符串

## 正则表达式语法

### 特殊字符

特殊字符有：
- `?`  
    对它前面的正则式匹配 0 到 1 次重复。`ab?` 会匹配 `'a'` 或者 `'ab'`。

- `*?`, `+?`, `??`  
    `'*'`, `'+'` 和 `'?'` 数量限定符都是 *贪婪的*；它们会匹配尽可能多的文本：
    
    如果 RE `<.*>` 针对 `'<a> b <c>'` 进行匹配，它将匹配整个字符串，而不只是 `'<a>'`。
    
    在数量限定符之后添加 `?` 将使其以 *非贪婪* 或 *最小* 风格来执行匹配；也就是将匹配数量尽可能 *少的* 字符。使用 RE `<.*?>` 将只匹配 `'<a>'`。

- `(...)`  
    捕获组，匹配圆括号内的任意正则表达式

- `(?P<name>…)`  
    命名捕获组，使用 `name` 作为 `key` 访问字典

### 特殊序列

由 `'\'` 和一个字符组成的特殊序列在以下列出。

- `\w`  
    - 字符串型 `str`  
        匹配 Unicode 单词类字符，这包括所有 Unicode 字母数字类字符 (由 `[str.isalnum()]` 定义)，以及下划线 (`_`)

    - 字节串型 `bytes`  
        匹配在 ASCII 字符集中被视为字母数字的字符 `[a-zA-Z0-9_]`

- `\W`  
    匹配不属于单词类字符的任意字符，与 `\w` 相反。

## 模块内容

模块定义了几个函数、常量，和一个异常。

### 标志

#### class re.RegexFlag

包含以下列出的正则表达式选项的 `enum.IntFlag` 类。

- `re.DOTALL`  
    使 `'.'` 特殊字符匹配任意字符，包括换行符 `\n`；如果没有这个旗标，`'.'` 将匹配 除去 换行符以外的任意字符。

    对应于内联旗标 `(?s)`。

- 
    ```py
    re.U
    re.UNICODE
    ```
    在 Python 3 中，`str` 模式默认将匹配 Unicode 字符。此旗标无任何效果，仅用于向下兼容。

### 函数

对于拥有 `flags` 参数的函数
- 表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

对于可返回空匹配的函数
- 即空串

#### re.compile() —— 编译正则表达式模式为对象

```python
re.compile(pattern, flags=0)
```

将正则表达式模式编译为一个正则表达式对象，可以被用于通过这个对象的方法 `match()`、`search()` 以及如下所述的其他方法进行匹配。

```python
# 序列
prog = re.compile(pattern)
result = prog.match(string)

# 等价于
result = re.match(pattern, string)
```

如果需要多次使用这个正则表达式的话，使用 `re.compile()` 和保存这个正则对象以便复用，可以让程序更加高效。

> 通过 `re.compile()` 编译后的样式，和模块级的函数会被缓存，所以少数的正则表达式使用无需考虑编译的问题。

#### re.search() —— 任意位置查找第一个匹配

```python
re.search(pattern, string, flags=0)
```

扫描整个 *string* 查找正则表达式 *pattern* 产生匹配的第一个位置，并返回相应的 `Match`。如果字符串中没有与模式匹配的位置则返回 `None`

#### re.match() —— 从开头匹配

```python
re.match(pattern, string, flags=0)
```

如果 *string* 开头的零个或多个字符与正则表达式 *pattern* 匹配，则返回相应的 `Match`。如果字符串与模式不匹配则返回 `None`

注意即便是 `MULTILINE` 多行模式，`re.match()` 也只匹配字符串的开始位置，而不匹配每行开始。

如果你想定位 *string* 的任何位置，使用 `search()` 来替代（也可参考 `[search() vs. match()]`）。

#### re.fullmatch() —— 完全匹配

```python
re.fullmatch(pattern, string, flags=0)
```

如果整个 *string* 与正则表达式 *pattern* 匹配，则返回相应的 `Match`。如果字符串与模式不匹配则返回 `None`

#### re.findall() —— 查找所有非重叠匹配，返回列表

```python
re.findall(pattern, string, flags=0)
```

返回 *pattern* 在 *string* 中的所有非重叠匹配，以字符串列表或字符串元组列表的形式。对 *string* 的扫描从左至右，匹配结果按照找到的顺序返回。空匹配也包括在结果中。

返回结果取决于模式中捕获组的数量。如果没有组，返回与整个模式匹配的字符串列表。如果有且仅有一个组，返回与该组匹配的字符串列表。如果有多个组，返回与这些组匹配的字符串元组列表。非捕获组不影响结果。

```pycon
# 普通匹配模式
>>> re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
['foot', 'fell', 'fastest']

# 捕获组模式
>>> re.findall(r'(\w+)=(\d+)', 'set width=20 and height=10')
[('width', '20'), ('height', '10')]
```

#### re.finditer() —— 查找所有非重叠匹配，返回 Match 迭代器

```python
re.finditer(pattern, string, flags=0)
```

针对正则表达式 *pattern* 在 *string* 里的所有非重叠匹配返回一个产生 `Match` 对象的 `iterator`。*string* 将被从左至右地扫描，并且匹配也将按被找到的顺序返回。空匹配也会被包括在结果中。

```py
# 创建迭代器后，将组匹配的多个字段保存为字典，存入列表
regex_iter = re.finditer(re_pattern, origin_data)
regex_list = [regex_match.groupdict() for regex_match in regex_iter]
```

## 匹配对象

匹配对象总是有一个布尔值 `True`。如果没有匹配的话 `match()` 和 `search()` 返回 `None` 

```py
# 使用 if 快速判断是否匹配
match = re.search(pattern, string)
if match:
    process(match)
```

### class re.Match

```py
class re.Match
```
由成功的 `match` 和 `search` 所返回的匹配对象。

### Match.group()

```py
Match.group([group1, ...])
```
返回一个或者多个匹配的子组。 

参数数量
- 一个参数，返回一个字符串
- 多个参数，返回一个元组且其中每项都对应一个参数。 

参数值
- 一个正整数，返回组匹配的字符串。 
- 若一个分组号为负数或大于在模式中定义的分组数，则引发 `IndexError` 异常。 

如果正则表达式使用了 `(?P<name>...)` 命名组语法， `groupN` 参数可使用命名组的名字或索引值引用。

```pycon
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.group('first_name')
'Malcolm'
>>> m.group(1)
'Malcolm'
```

### `Match.__getitem__()` —— 索引匹配

```py
Match.__getitem__(g)
```
索引匹配，等价于 `m.group(g)`

> burp 的扩展增强插件无法使用切片，仅可的使用 `.group(g)`
> - 或由于 jpython 或 python 2.x

### Match.groupdict(default=None)

```py
Match.groupdict(default=None)
```
返回一个字典，包含了所有的 *命名* 子组。`key` 为组名。例如

```pycon
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.groupdict()
{'first_name': 'Malcolm', 'last_name': 'Reynolds'}
```

