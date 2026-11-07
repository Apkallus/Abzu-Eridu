# base64 --- Base16, Base32, Base64, Base85 数据编码

https://docs.python.org/zh-cn/3/library/base64.html

该模块提供了用于将二进制数据编码为可打印 ASCII 字符以及将此类编码解码回二进制数据的函数。这包括 [RFC 4648] 中 [指定的编码] （Base64、Base32 和 Base16）， [PDF 2.0] 中指定的 [Base85] 编码 ，以及在其他地方使用的非标准 Base85 变体。

[旧式接口] 不支持对字符串的解码，但它提供了用于编码和解码 [文件对象] 的函数。

## RFC 4648 编码格式

### base64.b64encode() —— 对类字节对象进行 base64 编码

```py
base64.b64encode(s, altchars=None, *, padded=True, wrapcol=0)
```

对 [bytes-like object] s 进行 Base64 编码，并返回编码后的 bytes。

- `altchars` 
    一个长度为 2 的 bytes-like object，指定用于替换 Base64 默认字符 `+` 和 `/` 的字符表。

- `padded`
    是否添加填充字符 `=` 使得数据长度为 4 的倍数

###  base64.b64decode()

```py
base64.b64decode(s, altchars=None, validate=False, *, padded=True, canonical=False)
base64.b64decode(s, altchars=None, validate=True, *, ignorechars, padded=True, canonical=False)
```

解码 Base64 编码过的 bytes-like object 或 ASCII 字符串 `s` 并返回解码过的 bytes


#### base64.urlsafe_b64encode(s, *, padded=True)

```py
base64.urlsafe_b64encode(s, *, padded=True)
```

使用 URL 与文件系统安全的字母表编码：使用 `-` 以及 `_` 代替标准 Base64 字母表中的 `+` 和 `/`

#### base64.urlsafe_b64decode(s, *, padded=False)

```py
base64.urlsafe_b64decode(s, *, padded=False)
```

使用 URL 与文件系统安全的字母表解码：使用 `-` 以及 `_` 代替标准 Base64 字母表中的 `+` 和 `/`


## 旧式接口

### base64.decode()

```py
base64.decode(input, output)
```

解码二进制 `input` 文件的内容并将结果二进制数据写入 `output` 文件。 `input` 和 `output` 必须为 [文件对象]

`input` 将被读取直至 `input.readline()` 返回空字节串对象。

### base64.encode()

```py
base64.encode(input, output)
```

编码二进制 `input` 文件的内容并将经 base64 编码的数据写入 `output` 文件。 `input` 和 `output` 必须为 [文件对象]。 

`input` 将被读取直到 `input.read()` 返回空字节串对象。 

`encode()` 会在每输出 76 个字节之后插入一个换行符 `b'\n'`，并会确保输出总是以换行符来结束，如 [RFC 2045 (MIME)] 所规定的那样。