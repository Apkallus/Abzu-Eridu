### 进制编码

Python 有两种类字符串常量：`str` 字符串（表示为 `"asdf"`）和 `bytes` 字节串（表示为 `b"asdf"`）。

对于数值常量，Python 的表示法是在二进制数据前加 `0b`，十六进制前加 `0x`，十进制保持不变，因此 `11 == 0b1011 == 0xb`

对于 `bytes`可以使用*转义序列*来指定它们。转义序列以 `\x` 开头，后跟两个十六进制数字，从而将一个具有该值的单个字节放入 `bytes` 常量中！

其他一些可能有用的 Python 特性：
- 如果你用 `print(n)` 打印一个数字或用 `str(n)` 将其转换为字符串，该数字将以十进制表示。
- 你可以使用 `hex(n)` 获取数字的十六进制字符串表示。
- 你可以使用 `bin(n)` 获取数字的二进制字符串表示。

### bytes

`bytes.fromhex(string: str,) -> bytes`

Example: `bytes.fromhex('B9 01EF')` -> `b'\xb9\x01\xef'`.

### sys

- `sys.argv`
    一个列表，其中包含了被传递给 Python 脚本的命令行参数。 `argv[0]` 为脚本的名称（是否是完整的路径名取决于操作系统）。
- `sys.stdout.buffer.write()`  
    `sys.stdin.buffer.read()`
    原始字节接口，使用二进制形式读写，类型为 `bytes`，即 `b"foo"`

### os
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

### frontmatter
- <https://python-frontmatter.readthedocs.io/en/latest/>
- ```frontmatter.load()```
    从文件名、文件中加载到对象 ```Post```
- ```frontmatter.loads()```
    加载字符串到对象 ```Post```

- ```post.content``` 或 ```post```
    访问元数据外的内容
- ```post.metadata```
    获取元数据字典
- ```post['元数据字段名']```
    从元数据字典中检索字段


### re

- <https://docs.python.org/zh-cn/3/library/re.html#>

- `r"内容"`  
    正则表达式使用反斜杠字符 ('\') 表示特殊形式或是允许在使用特殊字符时不引发它们的特殊含义。即，正则表达式使用反斜杠的字面量。  
    `r`前缀确保反斜杠不必做任何特殊处理。 因此 r"\n" 表示包含 '\' 和 'n' 两个字符的字符串。
- ```re.compile(pattern, flags=0)```
    将正则表达式保存到对象中复用
- `re.escape(pattern)`  
    在 pattern 中转义特殊字符。
- ```flags```
    - ```re.DOTALL```
    使 ```.``` 匹配包含 ```\n``` 在内的任意字符
- `re.sub(pattern, repl, string, count=0, flags=0)`  
    返回通过使用 repl 替换在 string 最左边非重叠出现的 pattern 而获得的字符串。 如果样式没有找到，则不加改变地返回 string。  
    可选参数 count 是要替换的模式的最大出现次数；count 必须是一个非负整数。 如果省略或为零，则将全部替换。
    - pattern 是 正则；
    - repl 如果是字符串，就是 正则替换模板，`\1` `/` `\g<name>` `/` `\n` 等会被再次解析；
    - repl 如果是函数，则返回值完全按字面量写入，不会再做任何转义解析。

    替换报错时，检查repl是否使用了字符串模式且未转义，于是可能被解析的字符使用函数模式。
    pattern 里通过 `re.escape` 把占位符当字面量；

- ```re.search()```
    在字符串的任意位置匹配模式，返回第一个匹配的 ```Match``` 或 ```None```

- ```Match.group([group1, ...])```
    单个参数返回字符串，多个参数返回元组
    参数 ```0``` 应用所有子分组的匹配，其他数字则返回对应子分组的匹配

- 正则表达式
    - ```*?``` ```+?``` ```??```
        在默认贪婪的匹配符后的 ```?``` 转为非贪婪模式
    - `{m,n}`  
        对正则式进行 m 到 n 次匹配，在 m 和 n 之间取尽量多。  
        忽略 m 意为指定下界为 0，忽略 n 指定上界为无限次。

由 '\' 和一个字符组成的特殊序列：
- `\s`
    匹配空白字符
    
### zipfile

[文档](https://docs.python.org/zh-cn/3/library/zipfile.html)

- `ZipFile.write(filename, arcname=None, compress_type=None, compresslevel=None)`
    将名为 filename 的文件写入归档，给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)。
- `ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, compresslevel=None)`
    将一个文件写入归档，内容为 data。 zinfo_or_arcname 可以是它在归档中将被给予的名称，或者是 ZipInfo 的实例。
    即，设置归档内文件名及其数据。

### string

- `string.replace(old, new[, count])`  
    使用字串new替换字串old  
    count设置替换次数，若未指定则替换所有

#### f-string

`f'...{val:08b}...'`

格式说明 `:`  
`:[[fill]align][sign][#][0][width][grouping_option][.precision][type]`
- `0`：如果不够 8 位，用 0 在左侧补齐。
- `8`：宽度为 8 个字符。
- `b`：以二进制形式输出，只包含 0/1。


### urllib

`urllib.request.urlopen(url, data=None, [timeout, ]*, context=None)`
打开 *url*，它可以是包含有效、正确编码的 URL 的字符串，也可以是 Request 对象。

```python
import urllib.request

url = 'https://www.example.com'
response = urllib.request.urlopen(url)
# 此处读取为字节序列，或需使用 decode('utf-8') 解码
content = response.read()

print(content)
```

### set

`set(s)`：将可迭代对象 s（如字符串、列表）转换为集合，自动去重

`{"a", "b"}`：创建一个包含字符 "a" 和 "b" 的集合。

操作符:
- `<=` ：检查左侧集合是否是右侧集合的子集

### int

使用 `int(s)` 将字符串转换为数字默认会将其读取为十进制数字。

你可以使用第二个参数指定不同的进制：`int(s, 16)` 将把字符串解释为十六进制，`int(s, 2)` 将把它解释为二进制。

你可以尝试使用 `int(s, 0)` 自动识别数字的进制，这需要字符串带有前缀（二进制用 `0b`，十六进制用 `0x`，十进制无前缀）。

方法：
- `to_bytes(self, length: int, byteorder: str, *, signed: bool=...) -> bytes`

### base64

```py
import base64
encoded = base64.b64encode(b'data to be encoded')
encoded
b'ZGF0YSB0byBiZSBlbmNvZGVk'
data = base64.b64decode(encoded)
```

- `base64.b64decode(data) -> bytes` ， data 可以是 bytes 或 str
    - 如果传 bytes：这些 bytes 应该是 ASCII 字符（比如 b"QUJD"）。
    - 如果传 str：这个 str 里也应该是 ASCII 字符（比如 "QUJD"）。
- `base64.b64encode(bytes) -> bytes`

### urllib

```python
import urllib.request
import urllib.parse

target_url = 'http://localhost:80/foo?bar=aaa'
method = 'POST'
data =  urllib.parse.urlencode({'name': 'value'}).encode()
req = urllib.request.Request(target_url, method=method, data=data)
req.add_header('User-Agent', 'Firefox')
req.add_header('Host', 'localhost:80')

resp = urllib.request.urlopen(req)
resp_headers = resp.headers
resp_body = resp.read().decode('utf-8')

print(resp_headers)
print(resp_body)
```

#### urllib.request

- `urllib.request.urlopen(url, data=None, [timeout, ]*, context=None)`  
    此函数始终返回一个可以作为 context manager 工作的对象，并具有 *url*、*headers* 和 *status* 属性。

- `class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`  
    这个类是 URL 请求的抽象。  
    - `Request.add_header(key, val)`  
        向请求添加另一个头部。

#### urllib.parse

- `urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus) -> str`  
    生成表单参数的名值对字符串  
    - `query: Union[Mapping[Any, Any], Mapping[Any, Sequence[Any]], Sequence[Tuple[Any, Any]], Sequence[Tuple[Any, Sequence[Any]]]]`  
        ```py
        urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        ```
    - `data` 为表单参数名值对的str编码后到bytes类型

    如果生成的字符串要用作 `urlopen()` 函数的 POST 操作的 data，则应将其编码为字节，否则会引发 TypeError。

#### urllib.response

- `url`  
    检索到的资源的 URL，通常用于确定是否发生了重定向。
- `headers`  
    以 `EmailMessage` 实例的形式返回响应头。
- `status`  
    服务器返回的状态码。

### requests

<https://requests.readthedocs.io/en/latest/>

#### requests.Session()

Session对象允许您将某些参数持久化 请求。它还在所有请求中持久化cookie 会话实例，并将使用连接池。

```python
s = requests.Session()
r = s.get("http://localhost:80/foosetcookie")
print(r.headers)
r = s.get("http://localhost:80/barcarrycookie")
print(r.headers)
print(r.text)
```

### flask

<https://flask.palletsprojects.com/zh-cn/stable/quickstart/#a-minimal-application>

```python
import flask

app = flask.Flask(__name__)
    
@app.route("/", methods=["GET"])
def index():
    return flask.redirect('http://challenge.localhost:80/gate', 302)

app.secret_key = os.urandom(8)
app.run("localhost", 1337)
```

### 备忘

- ```with open(filepath, 'r', encoding='utf-8') as f:```
    设置文件路径、模式、编码后读取文件，作用域结束后自动关闭
    - `x` 模式可避免覆盖文件

- ```if not container:```
    在布尔上下文快速判断字典、列表、元组等容器是否为空

- `'abcde'[1:]`
    提取子串

- `for i, value in enumerate(列表)`  
    `enumerate()` 函数返回下标与值，可用来遍历列表

- `print(foo, end="")`
    设置换行

- `assert condition, error_message`
    - condition：需验证的条件表达式，结果为 True 或 False。
    - error_message：可选参数，当条件为 False 时抛出的异常提示信息

## 参考

https://geek-docs.com/python