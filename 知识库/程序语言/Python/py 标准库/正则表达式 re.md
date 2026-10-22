# re --- 正则表达式操作

https://docs.python.org/zh-cn/3.14/library/re.html

- `r"内容"`  
    正则表达式使用反斜杠字符 ('\') 表示特殊形式或是允许在使用特殊字符时不引发它们的特殊含义。即，正则表达式使用反斜杠的字面量。  
    `r`前缀确保反斜杠不必做任何特殊处理。 因此 r"\n" 表示包含 '\' 和 'n' 两个字符的字符串。

- `flags`
    - `re.DOTALL`
    使 `.` 匹配包含 `\n` 在内的任意字符

tips:
- 末尾使用非贪婪模式可导致匹配失败返回空串

## 正则表达式语法

特殊字符有：
- `?`
    对它前面的正则式匹配 0 到 1 次重复。

- `*?`, `+?`, `??`
    在数量限定符之后添加 `?` 将使其以 非贪婪 或 最小 风格来执行匹配；

## 匹配对象

匹配对象总是有一个布尔值 `True`。如果没有匹配的话 `match()` 和 `search()` 返回 `None` 

```py
# 使用 if 快速判断是否匹配
match = re.search(pattern, string)
if match:
    process(match)
```

```py
class re.Match
```
- 由成功的 `match` 和 `search` 所返回的匹配对象。

```py
Match.group([group1, ...])
```
- 返回一个或者多个匹配的子组。 如果只有一个参数，结果就是一个字符串；如果有多个参数，结果就是一个元组且其中每项都对应一个参数。 

```py
Match.__getitem__(g)
```
- 索引匹配，等价于 `m.group(g)`
> burp 的扩展增强插件无法使用切片，仅可的使用 `.group(g)`
> - 猜测由于 jpython 或 python 2.x

## 模块内容

### 函数

#### `re.compile` —— 编译正则表达式模式为对象

```python
re.compile(pattern, flags=0)
```

将正则表达式模式编译为一个正则表达式对象，可以被用于通过这个对象的方法 `match()`、`search()` 以及如下所述的其他方法进行匹配。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

序列

```python
prog = re.compile(pattern)
result = prog.match(string)
```

等价于

```python
result = re.match(pattern, string)
```

如果需要多次使用这个正则表达式的话，使用 `re.compile()` 和保存这个正则对象以便复用，可以让程序更加高效。

> **备注**
> 通过 `re.compile()` 编译后的样式，和模块级的函数会被缓存，所以少数的正则表达式使用无需考虑编译的问题。

#### `re.search` —— 任意位置查找第一个匹配

```python
re.search(pattern, string, flags=0)
```

扫描整个 *string* 查找正则表达式 *pattern* 产生匹配的第一个位置，并返回相应的 `Match`。如果字符串中没有与模式匹配的位置则返回 `None`；请注意这不同于在字符串的某个位置上找到零长度匹配。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

#### `re.match` —— 从开头匹配

```python
re.match(pattern, string, flags=0)
```

如果 *string* 开头的零个或多个字符与正则表达式 *pattern* 匹配，则返回相应的 `Match`。如果字符串与模式不匹配则返回 `None`；请注意这与零长度匹配是不同的。

注意即便是 `MULTILINE` 多行模式，`re.match()` 也只匹配字符串的开始位置，而不匹配每行开始。

如果你想定位 *string* 的任何位置，使用 `search()` 来替代（也可参考 search() vs. match()）。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

#### `re.fullmatch` —— 完全匹配

```python
re.fullmatch(pattern, string, flags=0)
```

如果整个 *string* 与正则表达式 *pattern* 匹配，则返回相应的 `Match`。如果字符串与模式不匹配则返回 `None`；请注意这与零长度匹配是不同的。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

在 3.4 版本新增。

#### `re.split` —— 正则分割字符串

```python
re.split(pattern, string, maxsplit=0, flags=0)
```

用 *pattern* 分开 *string*。如果在 *pattern* 中捕获到括号，那么所有的组里的文字也会包含在列表里。如果 *maxsplit* 非零，最多进行 *maxsplit* 次分隔，剩下的字符全部返回到列表的最后一个元素。

```py
>>> re.split(r'\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
>>> re.split(r'(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']
>>> re.split(r'\W+', 'Words, words, words.', maxsplit=1)
['Words', 'words, words.']
>>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
['0', '3', '9']
```

如果分隔符里有捕获组合，并且匹配到字符串的开始，那么结果将会以一个空字符串开始。对于结尾也是一样

```py
>>> re.split(r'(\W+)', '...words, words...')
['', '...', 'words', ', ', 'words', '...', '']
```

这样的话，分隔组将会出现在结果列表中同样的位置。

相邻的空匹配没有可能，但一个空匹配可以在一个非空匹配之后立即发生。

```py
>>> re.split(r'\b', 'Words, words, words.')
['', 'Words', ', ', 'words', ', ', 'words', '.']
>>> re.split(r'\W*', '...words...')
['', '', 'w', 'o', 'r', 'd', 's', '', '']
>>> re.split(r'(\W*)', '...words...')
['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
```

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

在 3.1 版本发生变更：增加了可选标记参数。

在 3.7 版本发生变更：增加了空字符串的样式分隔。

自 3.13 版本弃用：以位置参数形式传入 *maxsplit* 和 *flags* 的做法已被弃用。在未来的 Python 版本中它们将为 仅限关键字形参。

#### ♾️ `re.findall` —— 查找所有非重叠匹配，返回列表

```python
re.findall(pattern, string, flags=0)
```

> 常用来在组匹配后，使用索引

返回 *pattern* 在 *string* 中的所有非重叠匹配，以字符串列表或字符串元组列表的形式。对 *string* 的扫描从左至右，匹配结果按照找到的顺序返回。空匹配也包括在结果中。

返回结果取决于模式中捕获组的数量。如果没有组，返回与整个模式匹配的字符串列表。如果有且仅有一个组，返回与该组匹配的字符串列表。如果有多个组，返回与这些组匹配的字符串元组列表。非捕获组不影响结果。

```py
>>> re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
['foot', 'fell', 'fastest']
>>> re.findall(r'(\w+)=(\d+)', 'set width=20 and height=10')
[('width', '20'), ('height', '10')]
```

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

在 3.7 版本发生变更：非空匹配现在可以在前一个空匹配之后出现了。

#### `re.finditer` —— 查找所有非重叠匹配，返回迭代器

```python
re.finditer(pattern, string, flags=0)
```

针对正则表达式 *pattern* 在 *string* 里的所有非重叠匹配返回一个产生 `Match` 对象的 iterator。*string* 将被从左至右地扫描，并且匹配也将按被找到的顺序返回。空匹配也会被包括在结果中。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

在 3.7 版本发生变更：非空匹配现在可以在前一个空匹配之后出现了。

#### `re.sub` —— 正则字符串替换

```python
re.sub(pattern, repl, string, count=0, flags=0)
```

返回通过使用 *repl* 替换在 *string* 最左边非重叠出现的 *pattern* 而获得的字符串。如果样式没有找到，则不加改变地返回 *string*。*repl* 可以是字符串或函数；如为字符串，则其中任何反斜杠转义序列都会被处理。也就是说，`\n` 会被转换为一个换行符，`\r` 会被转换为一个回车符，依此类推。未知的 ASCII 字符转义序列保留在未来使用，会被当作错误来处理。其他未知转义序列例如 `\&` 会保持原样。向后引用像是 `\6` 会用样式中第 6 组所匹配到的子字符串来替换。例如：

```py
>>> re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(\s*\):',
...        r'static PyObject*\npy_\1(void)\n{',
...        'def myfunc():')
'static PyObject*\npy_myfunc(void)\n{'
```

如果 *repl* 是一个函数，则它会针对每次 *pattern* 的非重叠出现的情况被调用。该函数接受单个 `Match` 参数，并返回替换字符串。例如：

```py
>>> def dashrepl(matchobj):
...     if matchobj.group(0) == '-': return ' '
...     else: return '-'
...
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'
>>> re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)
'Baked Beans & Spam'
```

模式可以是一个字符串或者 `Pattern`。

可选参数 *count* 是要替换的模式的最大出现次数；*count* 必须是一个非负整数。如果省略或为零，则将全部替换。

相邻的空匹配没有可能，但一个空匹配可以在一个非空匹配之后立即发生。因此，`sub('x*', '-', 'abxd')` 将返回 `'-a-b--d-'` 而不是 `'-a-b-d-'`。

在字符串类型的 *repl* 参数中，除了如上所述的字符转义和后向引用，`\g<name>` 还会使用由 `name` 指明的分组所匹配的子字符串，就像 `(?P<name>...)` 语法所定义的。`\g<number>` 使用相应的分组编号；因此 `\g<2>` 就等价于 `\2`，但在像 `\g<2>0` 这样的替换中避免了歧义。`\20` 将被解读为对分组 20 的引用，而不是对后面跟有字符字面值 `'0'` 的分组 2 的引用。后向引用 `\g<0>` 会在 RE 所匹配的整个子字符串中进行替换。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

在 3.1 版本发生变更：增加了可选标记参数。

在 3.5 版本发生变更：不匹配的组合替换为空字符串。

在 3.6 版本发生变更：*pattern* 中的未知转义（由 `'\'` 和一个 ASCII 字符组成）被视为错误。

在 3.7 版本发生变更：在 *repl* 中由 `'\'` 加一个 ASCII 字母组成的未知转义序列现在将导致错误。一个空匹配可以在一个非空匹配之后立即发生。

在 3.12 版本发生变更：分组 *id* 只能包含 ASCII 数码。在 `bytes` 替换字符串中，分组 *name* 只能包含 ASCII 范围内的字节值（`b'\x00'`-`b'\x7f'`）。

自 3.13 版本弃用：以位置参数形式传入 *count* 和 *flags* 的做法已被弃用。在未来的 Python 版本中它们将为 仅限关键字形参。

#### `re.subn` —— 正则字符串替换，返回元组

```python
re.subn(pattern, repl, string, count=0, flags=0)
```

行为与 `sub()` 相同，但是返回一个元组 `(字符串，替换次数)`。

表达式的行为可通过指定 *flags* 值来修改。值可以是任意 `flags` 变量，可使用按位 OR（`|` 运算符）进行组合。

#### `re.escape` —— 正则转义

```python
re.escape(pattern)
```

转义 *pattern* 中的特殊字符。如果你想对任意可能包含正则表达式元字符的文本字符串进行匹配，它就是有用的。比如

```py
>>> print(re.escape('https://www.python.org'))
https://www\.python\.org

>>> legal_chars = string.ascii_lowercase + string.digits + "!#$%&'*+-.^_`|~:"
>>> print('[%s]+' % re.escape(legal_chars))
[abcdefghijklmnopqrstuvwxyz0123456789!\#\$%\&'\*\+\-\.\^_`\|\~:]+

>>> operators = ['+', '-', '*', '/', '**']
>>> print('|'.join(map(re.escape, sorted(operators, reverse=True))))
/|\-|\+|\*\*|\*
```

这个函数不能被用于 `sub()` 和 `subn()` 的替换字符串，只有反斜杠应该被转义。例如：

```py
>>> digits_re = r'\d+'
>>> sample = '/usr/sbin/sendmail - 0 errors, 12 warnings'
>>> print(re.sub(digits_re, digits_re.replace('\\', r'\\'), sample))
/usr/sbin/sendmail - \d+ errors, \d+ warnings
```

在 3.3 版本发生变更：`'_'` 不再被转义。

在 3.7 版本发生变更：只有在正则表达式中具有特殊含义的字符才会被转义。因此，`'!'`、`'"'`、`'%'`、`"'"`、`','`、`'/'`、`':'`、`';'`、`'<'`、`'='`、`'>'`、`'@'` 和 `` "`" `` 将不再会被转义。

#### `re.purge` —— 清除正则表达式的缓存

```python
re.purge()
```

清除正则表达式的缓存。