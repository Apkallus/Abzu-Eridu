# unicodedata --- Unicode 数据库

https://docs.python.org/zh-cn/3.15/library/unicodedata.html

本模块提供对 Unicode 字符数据库（UCD）的访问，该数据库为所有 Unicode 字符定义字符属性。

### unicodedata.lookup() —— 名称到字符

```py
unicodedata.lookup(name, /)
```

按名称查找字符

```py
unicodedata.lookup('LEFT CURLY BRACKET')
# '{'
```

此函数返回的字符与字符串字面值中 `\N` 转义序列生成的字符相同。例如:

```py
unicodedata.lookup('MIDDLE DOT') == '\N{MIDDLE DOT}'
# True
```

### unicodedata.name() —— 字符到名称

```py
unicodedata.name(chr, default=None, /)
```

返回分配给字符 chr 的名称（字符串形式）

```py
unicodedata.name('½')
# 'VULGAR FRACTION ONE HALF'
unicodedata.name('\uFFFF', 'fallback')
# 'fallback'
```