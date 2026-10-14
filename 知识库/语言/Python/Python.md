https://docs.python.org

### venv — 创建虚拟环境

```sh
python3 -m venv 虚拟环境路径

source 虚拟环境路径/bin/activate # 激活虚拟环境

deactivate # 退出当前虚拟环境
```

当从虚拟环境内部使用时，像 pip 这样的常用安装工具将把 Python 包安装到虚拟环境中，而无需显式告知。

若使用旧版 python 的虚拟环境，需安装 `python3.x-venv` 组件

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
    
- `.zfill(N)`
    补前导0到N

### bytearray

使用 bytearray() 对 bytes 进行处理，可执行切片赋值。

然而，单个索引赋值必须是一个 0–255 的整数，不能是 bytes 对象。


### struct 

```py
import struct

class cimg:
    MAGIC = b"CNNR"
    RENDER_FRAME =  struct.pack("<H", 1)
    RENDER_PATCH =  struct.pack("<H", 2)
    CREATE_SPRITE = struct.pack("<H", 3)
    RENDER_SPRITE = struct.pack("<H", 4)
    LOAD_SPRITE =   struct.pack("<H", 5)
    FLUSH =         struct.pack("<H", 6)
    SLEEP =         struct.pack("<H", 7)
```

`struct.pack(format, v1, v2, ...)`

格式字符串：
- `<`：小端序（little-endian）。
- `>`：大端序（big-endian），也称作网络字节序。
- `!`：网络字节序（等同于 >）。
- 默认（不写）则使用系统原生字节序。




### aiohttp - 异步网络模块

https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession

- `aiohttp.ClientSession()` 
    创建客户端异步网络对象，之后传递此对象使用其方法即进行异步网络通信

- `async ClientSession.get()`
    创建未实现的网络请求

- `await ClientResponse.json()`
    等待响应

```py
async with aiohttp.ClientSession() as net_session:


async with net_session.get(api_str) as response:
    response_json = await response.json()
```

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
- `sys.exit([arg])`  
    引发一个 `SystemExit` **异常**，表示想要退出解释器。  

    可选参数 `arg` 可以是一个表示退出状态的整数（默认值为 `0`），也可以是其他类型的对象。如果 `arg` 是整数，`0` 表示“成功终止”，任何非零值在 shell 等环境中被视为“异常终止”。大多数系统要求该值在 0–127 范围内，超出范围会导致未定义行为。有些系统为特定的退出码赋予了特定含义，但这些约定通常并不完善；Unix 程序通常使用 `2` 表示命令行语法错误，使用 `1` 表示其他类型的错误。如果传入其他类型的对象，`None` 等价于传入 `0`，而其他任何对象会被打印到 `stderr`，并导致退出码为 `1`。特别地，`sys.exit("some error message")` 是在发生错误时快速退出程序的一种方式。  

    由于 `exit()` 本质上“只是”引发一个异常，因此只有当它从主线程调用且该异常未被捕获时，才会真正退出进程。`try` 语句的 `finally` 子句所指定的清理操作仍然会执行，并且可以在外层代码中捕获这个退出尝试。


### shutil — 高级文件操作

- `shutil.rmtree(path, ignore_errors=False, onerror=None, *, onexc=None, dir_fd=None)`
    删除整个目录树；path 必须指向一个目录（但不是指向目录的符号链接）


    
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


    
### zipfile

[文档](https://docs.python.org/zh-cn/3/library/zipfile.html)

- `ZipFile.write(filename, arcname=None, compress_type=None, compresslevel=None)`
    将名为 filename 的文件写入归档，给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)。
- `ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, compresslevel=None)`
    将一个文件写入归档，内容为 data。 zinfo_or_arcname 可以是它在归档中将被给予的名称，或者是 ZipInfo 的实例。
    即，设置归档内文件名及其数据。



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

```py
from Crypto.Hash import SHA256

data = b"Hello, World!"

hash_object = SHA256.new(data=data)

# 获取原始二进制哈希值（32字节）
digest_bytes = hash_object.digest()

# 获取十六进制字符串表示
digest_hex = hash_object.hexdigest()
```

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
    原列表随机，不返回新列表

- `random.getrandbits(k)`
    返回具有 k 个随机比特位的非负 Python 整数。
        
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

### datetime

- `timedelta.total_seconds()`
    返回时间区间包含的总秒数。

### Numba 性能库

即时编译（Just-In-Time Compilation, JIT）

### 信号

```py
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
```

使用 `脚本 | head -n 50` 提取开头时，py 脚本并不退出而是持续 SIGPIPE 异常，此处设置 SIGPIPE 为默认状态从而结束进程

或使用 sed 命令，控制起始与结束
- `脚本 | sed -n '9000, 10000p'`

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


### concurrent.futures - threading 的包装库

https://docs.python.org/zh-cn/3.14/library/concurrent.futures.html



### dict

- `.items()`
    返回一个包含所有键值对的迭代器，每个键值对都是一个元组

- `dictionary.get(key, default)`
    通过键获取字典中的值。如果键存在于字典中，将返回对应的值；如果键不存在，将返回指定的默认值。

### list

- `list.remove(value)`
    按值删除元素
- `list.index()`
    获取第一个匹配索引
- `list.insert()`
    列表插入
- `list.extend(seq)`
    在列表末尾一次性追加另一个序列中的多个值

### 迭代器操作

- `map(lambad 元素: 元素操作, 迭代器)`
    map函数可以将一个函数应用于每一个元素，从而生成一个新的列表

### itertools 

https://docs.python.org/3/library/itertools.html

- `itertools.chain()` 函数将嵌套列表展开为一个平铺列表
- `itertools.product(*iterables, repeat=1)`
    生成迭代器的所有组合，懒加载

### ipaddress

https://docs.python.org/3/library/ipaddress.html#ipaddress.collapse_addresses

- `ipaddress.ip_network(, strict=False)`
    转化为库对象，当主机位不对齐时取消默认的严格模式 `strict` 

- `ipobj.hosts()`
    返回排除头尾后的可用 IP。遍历 ipobj 得到全部 IP

- `ipaddress.collapse_addresses(addresses)`
    设置 IP 对象后去重复

### match...case...

```py
match 判断条件:
    case 条件:
    case _:
```
### 特殊变量/函数

- `__name__ == '__main__'`
    区分直接执行与作为模块导入

    <https://docs.python.org/3/library/__main__.html>

    - 当导入一个 Python 模块或包时， `__name__` 会被设置为该模块或包的名称。
    - 如果该模块在顶层代码环境中执行，则其 `__name__` 设置为字符串 `'__main__' ` 


- `__file__`
    当前文件路径

- `__import__(模块字符串)`
    函数将导入模块，并返回模块对象（即，可使用 `.` 访问模块字段/方法）
    - 示例 `__import__('os').system('ls')`

### logging - 日志打印

https://docs.python.org/3/library/logging.html

```py
import logging

# 若省略 filename 则仅控制台输出
logging.basicConfig(
    filename='myapp.log', # 输出文件
    level=logging.INFO, # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s', # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S' # 时间格式
)
logging.debug("调试信息")   # 仅在 level 为 DEBUG 时输出
logging.info("info")   
logging.warning("warning") 
logging.error("error")   
```

### dataclasses - 设置类模板复用

<https://docs.pythonlang.cn/3/library/dataclasses.html>

```py
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

### pathlib

<https://docs.python.org/3/library/pathlib.html>

- `/`
    斜杠运算符用于创建子路径

- `Path(文件路径)`
    初始化路径对象
- `Path.absolute()`
    将路径设为绝对路径，不进行规范化或解析符号链接。返回一个新的路径对象
- `PurePath.parent`
    路径的逻辑父级
- `PurePath.is_absolute()`
    返回路径是否为绝对路径。
- `Path.is_file(*, follow_symlinks=True)`
    如果路径指向的是普通文件，则返回 True 。如果路径无效、无法访问或缺失，或者指向的不是普通文件，则返回 False 可以使用 Path.stat() 来区分这些情况。

    此方法通常会跟随符号链接；要排除符号链接，请添加参数 `follow_symlinks=False`

示例：
- `Path(__file__).absolute().parent`
    获取当前文件所在目录

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

- `[::-1]` 反转

- `dict_c = {**dict_a, **dict_b}` 
    字典展开，1个`*`为key展开，2个为键值对展开

- `.ljust(N, char)`
    使用选定字符左对齐N位

- `>>` 
    对整数的符号右移，即如果是正数则相当于无符号右移（由于 python int 的无限精度并带符号）

- `rev_list[0x11], rev_list[0x17] =  rev_list[0x17], rev_list[0x11]`
    列表元素快速交换

- 列表排序并需保持索引时，构建元组后使用匿名函数排序

- 匿名函数，默认从小到大排序，false < true
    - `test_list.sort(key=lambda x: (x < 5, x))`
        元素 >= 5 为第一组，元素 < 5 为第二组

- `对象.__name__`  
    查看对象名称
    
- `globals().get(name)` 
    `globals()[name]` 不存在会 KeyError  
    从全局变量与函数中查找对应字符串的对象

- `range(start, stop[, step])`
    范围的开始、结束、步长

- `sorted()`  
    返回排序后的新列表

- 在现存函数添加默认参数作为 flag，以添加新功能的同时，保持旧调用运行
    - 或拆分为多个函数，而不是添加 flag

- `:=` 
    象牙运算符，同时进行赋值与运算
    ```py
    if (n := len(lst)) > 0:
        print(n)
    ```

- `sum([[a,b], [c,d]], [空列表])` 
    进行列表加法，得到浅层列表扩展效果 `[空列表] + [a,b] + [c,d] = [a,b,c,d]`


## 各种格式文件数据解析

### json

`import json`

- `json.dumps()`  
    将python对象转为json格式的字符串，产生自带引号的字符串

- `json.load(fp, ...)`  
    将文件中的 json 内容反序列化转为 python 对象
- `json.loads(s, ...)`
    将 s (一个包含 JSON 的 str, bytes 或 bytearray 实例) 反序列化为 Python 对象。

### xml 

```python
import xml.etree.ElementTree as ET

tree = ET.parse(file_str) # 解析文件数据到对象
root = tree.getroot() # 得到根节点

for host in root.findall('host'): # 遍历所有 host 节点
    # 在 status 节点得到得到 state 字段
    state = host.find("status").get("state") 
```

### csv

```py
with open(f'{file_str}.csv', 'w', encoding='utf-8') as f:
    # 使用文件句柄与 csv 头部设置字典写入对象
    writer = csv.DictWriter(f, fieldnames=['addr', 'state', 'name'])
    # 写入头部与数据
    writer.writeheader()
    writer.writerows(data_list)
```
