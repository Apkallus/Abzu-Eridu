## 

### 进制编码

Python 有两种类字符串常量：`str` 字符串（表示为 `"asdf"`）和 `bytes` 字节串（表示为 `b"asdf"`）。

对于数值常量，Python 的表示法是在二进制数据前加 `0b`，十六进制前加 `0x`，十进制保持不变，因此 `11 == 0b1011 == 0xb`

常规可输入字符可直接放入 Python 字节字符串进行写入。
- `b"HELLO WORLD"`

对于 `bytes`可以使用*转义序列*来指定它们。转义序列以 `\x` 开头，后跟两个十六进制数字，从而将一个具有该值的单个字节放入 `bytes` 常量中
- `b"HELLO \x57\x4f\x52\x4c\x44"`

其他一些可能有用的 Python 特性：
- 如果你用 `print(n)` 打印一个数字或用 `str(n)` 将其转换为字符串，该数字将以十进制表示。
- 你可以使用 `hex(n)` 获取数字的十六进制字符串表示。
- 你可以使用 `bin(n)` 获取数字的二进制字符串表示。

### bytes

- `bytes.fromhex(string: str,) -> bytes`  
    Example: `bytes.fromhex('B9 01EF')` -> `b'\xb9\x01\xef'`.

- `bytes.hex()`  
    将bytes转为十六进制字符串

- `bytes(...)`  
    当参数是 “可迭代的整数序列” 时（比如列表、元组），bytes 会把每个整数当作一个字节（0–255），拼成一个 bytes 对象。  
    比如：`bytes((65, 66, 67)) == b"ABC"`。
    

### bytearray

使用 bytearray() 对 bytes 进行处理，可执行切片赋值。

然而，单个索引赋值必须是一个 0–255 的整数，不能是 bytes 对象。

### int

- `int.to_bytes()`   
    将数字转为字节，设置长度与大小端序（也可用 `struct` 包）
    ```py
    def to_bytes(self, length: int, byteorder: str, *, signed: bool=...) -> bytes
    ```
- `int.from_bytes(test_bytes, byteorder='little')`
    将bytes转为int

- `ord(asc_str)`：
    把单字符变成它的 ASCII 码，比如：
    `ord("c") == 99`

- `int(内容, 进制)`
    以选定进制转为int

### struct 

`struct.pack(format, v1, v2, ...)`

格式字符串：
- `<`：小端序（little-endian）。
- `>`：大端序（big-endian），也称作网络字节序。
- `!`：网络字节序（等同于 >）。
- 默认（不写）则使用系统原生字节序。


### subprocess 子进程管理

subprocess 模块允许你生成新的进程，连接它们的输入、输出、错误管道，并且获取它们的返回码。

推荐的调用子进程的方式是在任何它支持的用例中使用 run() 函数。对于更进阶的用例，也可以使用底层的 Popen 接口。

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

### scapy

<https://scapy.readthedocs.io/en/latest/>

基础使用：

- 堆叠层:
    `/` 运算符已被用作两层之间的组合运算符。这样做时，较低层的一个或多个默认字段可以根据较高层进行重载。一个字符串可以用作原始层。例：
    ```py
    Ether()/IP()/TCP()

    IP()/TCP()/"GET / HTTP/1.0\r\n\r\n"

    Ether()/IP()/IP()/UDP()
    ```

    堆叠对象使用 `.show2()` 方法展示字段

    当 Scapy 解析到某一层之后，剩下的字节它不知道该按什么协议解释时，就会把它放进一个通用层: `Raw`。
    - 对 TCP 来说，`Raw` 往往就是“应用层数据”。
        - 判断是否有应用层数据：`pkt.haslayer(scapy.Raw)`
        - 取出这段原始数据：`pkt[scapy.Raw].load`（类型是 `bytes`）

- 发送数据包:
    `send()`函数会在第 3 层发送数据包。也就是说，它会为你处理路由和第 2 层。
    `sendp()`函数会在第 2 层工作。你需要自己选择正确的接口和正确的链路层协议。
    如果将 return_packets=True 作为参数传递，send()和 sendp()也会返回发送的数据包列表。
    即，使用`send()`同时堆叠`Ether()`将报错

- 接收数据包：
    `sr1()` 函数发送并等待响应，返回响应内容

网络栈：

- 获取接口的 IP 地址
    ```py
    get_if_addr(conf.iface)  # default interface
    get_if_addr("eth0")
    ```

- 获取接口的 MAC 地址 
    ```py
    get_if_hwaddr(conf.iface)  # default interface
    get_if_hwaddr("eth0")
    ```

- 获取到达 IP 的下一跳的 MAC 地址
    ```py
    getmacbyip("10.0.0.1")
    ```

嗅探：
我们可以轻松捕获一些数据包，甚至可以克隆 tcpdump 或 tshark。可以提供一个接口或接口列表来进行嗅探。如果没有给出接口，嗅探将在 conf.iface 上进行。

```py
sniff(
    iface="eth0",                         # scapy.conf.iface
    filter="tcp port 31337 or arp",       # BPF 过滤
    prn=handle,                           # 抓包的处理函数
    store=False,                          # 不存内存
)
```

其他：
- `包.haslayer(scapy.Ether)` 判断是否存在对应网络层
- 删除  
    修改内容后使用删除后scapy自动重新计算
    ```py
    del pkt[scapy.IP].len
    del pkt[scapy.IP].chksum
    del pkt[scapy.TCP].chksum
    ```

### asyncio - 异步协程（协作式切换）

- `class asyncio.Semaphore(value=1)`  
    信号量：限制同一时刻最多允许多少个任务“进入临界区”

    使用 `Semaphore` 的推荐方式是通过 `async with` 语句（异步上下文管理器）。:
    如果内部计数器的值大于零，则将其减一并立即返回 True。 如果其值为零，则会等待直到 release() 并调用并返回 True。
    ```py
    sem = asyncio.Semaphore(10)

    # ... 稍后
    async with sem:
        # 操作共享的资源
    ```
- `create_task()`
    将协程对象创建并调度为一个任务来执行，返回一个 Task 对象。
    通常设置“任务数≈信号量”

- `await gather()`  
    聚合多个协程或 Future 对象的结果，返回一个汇总结果的 Future 对象。协程会被自动包装成 Future 并调度到事件循环中执行，但不保证调度顺序与传入顺序一致。

- `await asyncio.sleep()`
    非阻塞的暂停当前协程（秒）

- `await open_connection()`  
    异步建立 TCP 连接，返回 `(reader, writer)`
    - `reader` 用 `await reader.read(n)` 读取
    - `writer` 用 `writer.write(...)` + `await writer.drain()` 写入    
        - `writer.close()`  发起关闭
        - `await writer.wait_closed()` 等待关闭真正完成（缓冲刷出/FIN 发送/传输层状态清理等）


### collections

#### namedtuple

自动生成一个带字段名的 `tuple` 类

```py
from collections import namedtuple

Pixel = namedtuple("Pixel", ["ascii"])
p = Pixel(65)
```

此处：
- 生成一个新类，类名叫 Pixel
- 这个类的“字段”（成员）只有一个，名字叫 "ascii"
- 然后把这个类赋值给变量 Pixel，可以像普通类一样用它

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

- `os.urandom(n)`
    随机字节生成。  
    `secrets.token_bytes(n)` 为对应的安全封装函数

### json

- `json.dumps()`  
    将python对象转为json格式的字符串，产生自带引号的字符串

- `json.loads()`  
    将json内容转为python对象

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
- `re.findall(pattern, string, flags=0)`  
    返回 pattern 在 string 中的所有非重叠匹配，以字符串列表或字符串元组列表的形式。对 string 的扫描从左至右，匹配结果按照找到的顺序返回。 空匹配也包括在结果中。
- ```Match.group([group1, ...])```
    `re.Match` 对象的单个参数返回字符串，多个参数返回元组
    参数 ```0``` 应用所有子分组的匹配，其他数字则返回对应子分组的匹配

    ```py
    m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    m.group(0)       # 整个匹配

    m.group(1)       # 第一个圆括号标记的子分组。

    m.group(2)       # 第二个圆括号标记的子分组。

    m.group(1, 2)    # 使用多个参数则返回一个元组。
    ```
    
- `Match.groups(default=None)`
    返回一个元组，包含所有匹配的子组，在样式中出现的从1到任意多的组合。 default 参数用于不参与匹配的情况，默认为 None。
    注意，不包含 group 的整个匹配，仅为子分组。

    ```py
    m = re.match(r"(\d+)\.(\d+)", "24.1632")
    m.groups()
    ('24', '1632')
    ```

例如：
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

- 字符集
    - `string.ascii_letters` 大小写字母
    - `string.digits` 数字
    - `string.punctuation` 标点符号
    - `string.printable` 可打印字符
    

- `string.replace(old, new[, count])`  
    使用字串new替换字串old  
    count设置替换次数，若未指定则替换所有

- `chr()`  
    将ascii转为字符

- `.encode()`
    字符串转为bytes

#### f-string

`f'...{val:08b}...'`

格式说明 `:`  
`:[[fill]align][sign][#][0][width][grouping_option][.precision][type]`
- `0`：如果不够 8 位，用 0 在左侧补齐。
- `8`：宽度为 8 个字符。

进制：
- `b`：以二进制形式输出，只包含 0/1。
- `x`:十六进制

### PyCryptoDome

<https://pycryptodome.readthedocs.io/en/latest/>

`from Crypto.Util.strxor import strxor`
- `strxor()` 函数对两个字符串进行异或运算，消耗和产生的是字节
    
- `pad(data_to_pad: bytes, block_size: int, style: Optional[str]='pkcs7') -> bytes`
    填充

- `from Crypto.Random.random import getrandbits`  
    获得随机bytes

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

cipher = AES.new(key=key, mode=AES.MODE_CBC)
ciphertext = cipher.iv + cipher.encrypt(pad(flag, cipher.block_size))
```

#### RSA

```py
from Crypto.PublicKey import RSA
```

- `RSA.generate(bits: int, randfunc: Optional[RNG]=None, e: Optional[int]=65537) -> RsaKey`
    Create a new RSA key pair.

#### Hash

`from Crypto.Hash.SHA256 import SHA256Hash`

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

### random

- `random.randint(a, b)`  
    生成 [a, b] 范围内的整数（包含两端）。

- `random.uniform(a, b)` 
    生成 [a, b] 范围内的随机浮点数。

- `random.shuffle()`
    列表随机
    
### hashlib

`hashlib.sha256()`

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

target_url = 'http://localhost:80/x?'
method = 'POST'
# 查询参数构造为名值对字符串并进行url编码
query = urllib.parse.urlencode({'foo':"bar"})
target_url += query
# 表单内容构造为名值对并url编码后再编码为bytes，data必须是 bytes，否则报 TypeError。
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
    - 返回一个 类文件对象（`http.client.HTTPResponse` 的子类）
        - 支持 `read()`, `readline()`, `close()`
        - 也支持 `with` 上下文管理器
    
    并具有 *url*、*headers* 和 *status* 属性。  
    `data` 不为 `None` 时，`urlopen` 会自动使用 POST 方法

- `class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`  
    这个类是 URL 请求的抽象。   
    `data` 不为 `None` 时，`urlopen` 会自动使用 POST 方法
    - `Request.add_header(key, val)`  
        向请求添加另一个头部。

#### urllib.parse

- `urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus) -> str`  
    生成表单或查询参数的名值对字符串  
    - `query: Union[Mapping[Any, Any], Mapping[Any, Sequence[Any]], Sequence[Tuple[Any, Any]], Sequence[Tuple[Any, Sequence[Any]]]]`  
        ```py
        urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        ```
    - `data` 为表单参数名值对的str编码后到bytes类型

    如果生成的字符串要用作 `urlopen()` 函数的 POST 操作的 data，则应将其编码为字节，否则会引发 TypeError。

- `parse.quote()`  
    URL 编码
- `parse.unquote()`
    URL 解码

#### urllib.response

- `url`  
    检索到的资源的 URL，通常用于确定是否发生了重定向。

- `headers`  
    类字典对象的形式返回响应头。

    ```py
    resp.getheader('Content-Type')
    resp.headers['Content-Type']
    ```

- `resp.read()`
    返回 bytes，对于文本常见做法是 

    ```py
    resp.read().decode('utf-8')
    ```

- `status`  
    服务器返回的状态码。

### requests

<https://requests.readthedocs.io/en/latest/>

#### requests.Session()

Session对象允许您将某些参数持久化 请求。它还在所有请求中持久化cookie 会话实例，并将使用连接池。

- `requests.post(..., data={...})` 会把数据按 `application/x-www-form-urlencoded` 编码（等价于自动做一遍 URL 编码）。

```python
s = requests.Session()
s.cookies['cookie_name'] = 'cookie_value'
r = s.get("http://localhost:80/")

data = {'username': 'admin', 'password': "foo"}
r = s.post("http://challenge.localhost:80/", data=data, allow_redirects=False)

print(r.status_code)
print(r.headers)
print(r.text)
```

- `response = session.post(url, json=your_dict_data)`  
    使用post的 json 参数并传入字典以发送 json 数据

返回对象使用 `r.json()` 转为python对象

### Numba 性能库

即时编译（Just-In-Time Compilation, JIT）

### pwntools

设置timeout并满足时，将抛出异常。使用 `try ... except ...`

- `send()`  
    发送原始字节
    - `shutdown('send')`  
        发送 EOF 关闭 `send`

- `sendline()`
    发送一行数据，末尾添加换行符 `\n`
- `sendlineafter(delim, data, timeout=default)→ str`  
    在获得 `delim` 提示后，发送 `data` 数据

- `recv(n)`：
    最多读 n 字节（可能少于 n）
- `recvn(n)`：
    确保读满 n 字节（不够会等）
- `recvline(drop=False, timeout=default)→ bytes`  
    从管道中接收一行数据。  
    “一行”是指以 `newline` 中设置的字节序列终止的任意字节序列，默认值为 `b'\n'` 。

- `recvuntil(delims, drop=False, timeout=default)→ bytes`
    接收数据直到遇到其中一个分隔符，分隔符将被消耗。
    可与`recvline`组合，在收到提示数据后再读取。

- `recvall(timeout=Timeout.forever)`
    接收所有内容直到超时

- `p.clean(timeout=0.05)`
    把已有输出都读掉

示例：
```py
from pwn import process
from subprocess import STDOUT

p = process(["/challenge/run"], stderr=STDOUT)

p.sendlineafter(b'Choice? ', b'1')

p.recvuntil(b"Result: ")
line = p.recvline()
```

`from pwn import xor` 处理python原生不支持的bytes之间异或

### math

- `math.ceil()`  向上取整
- `math.gcd()` 判断是否互质

### http.server

```py
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.parse as up

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = up.urlparse(self.path).query
        print(time.strftime("%H:%M:%S"), self.path, qs, flush=True)
        self.send_response(204)   # No Content
        self.end_headers()

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 9999), H).serve_forever()
```

### threading

`from threading import Condition`

- `threading.Condition`：
    带锁的全局共享状态变量（锁/阻塞/唤醒）
    - `wait(timeout)` 阻塞直到被 `notify_all()` 唤醒或超时。
    - `wait_for(...)` 等待直到条件满足或超时

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

- `next(迭代器, 默认值)`  
    遍历迭代器，返回第一个匹配的元素。若不存在则返回默认值

- `reversed()`  
    迭代器的逆向

- `pow(base, exp, mod)`  
    快速横幂运算
    
- `raise`
    手动触发异常
    `raise ValueError("错误信息")`

- `_, a, b, _, c = 函数()`  
    使用`_` 忽略对应字段

- `global var`
    使用 `global` 前缀在函数中修改全局变量

## 参考

https://geek-docs.com/python