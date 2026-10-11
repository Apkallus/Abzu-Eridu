# 标准库

## 互联网协议和支持

---


### urllib

https://docs.python.org/zh-cn/3.14/library/urllib.request.html

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

    - 总会返回一个对象，该对象可作为 `context manager` 使用，带有 `url`、`headers` 和 `status` 属性

    - 对于 HTTP 和 HTTPS 的 URL 而言，返回一个类文件对象（`http.client.HTTPResponse` 的子类）
        - 支持 `read()`, `readline()`, `close()`
        - 也支持 `with` 上下文管理器
    
    - `data` 不为 `None` 时，`urlopen` 会自动使用 POST 方法

    > 旧版或存在 URL 参数注入：拼接字符串到 URL 参数后，主机可被覆盖；而 URI 设置换行符后可注入头部（使用字符串拼接，拥有 `HTTP/1.1` 版本后缀，需添加有效版本，并设置冗余头部吸收原后缀）

- `class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`  
    这个类是 URL 请求的抽象。   
    `data` 不为 `None` 时，`urlopen` 会自动使用 POST 方法
    - `Request.add_header(key, val)`  
        向请求添加另一个头部。

#### urllib.parse --- 将 URL 解析为组件

<https://docs.python.org/zh-cn/3.14/library/urllib.parse.html>

- `urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus) -> str`  
    生成表单或查询参数的名值对字符串  
    - `query: Union[Mapping[Any, Any], Mapping[Any, Sequence[Any]], Sequence[Tuple[Any, Any]], Sequence[Tuple[Any, Sequence[Any]]]]`  
        ```py
        urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        ```
    - `data` 为表单参数名值对的str编码后到bytes类型

    如果生成的字符串要用作 `urlopen()` 函数的 POST 操作的 data，则应将其编码为字节，否则会引发 TypeError。


- `parse.unquote()`
    URL 解码
    - python 2 对应函数 `urllib.unquote(string)`

##### URL 转码

URL 转码函数的功能是接收程序数据并通过对特殊字符进行转码并正确编码非 ASCII 文本来将其转为可以安全地用作 URL 组成部分的形式。 它们还支持逆转此操作以便从作为 URL 组成部分的内容中重建原始数据，如果上述的 URL 解析函数还未覆盖此功能的话。

###### urllib.parse.quote

```python
urllib.parse.quote(string, safe='/', encoding=None, errors=None)
```

使用 `%xx` 转义替换 *string* 中的特殊字符。字母、数字和字符 `'_.-~'` 永远不会被引用。默认情况下，此函数用于引用 URL 的路径部分。

- *string* 
    可以是 `str` 或 `bytes` 对象。

- 可选的 *safe* 参数
    指定了不应被引用的额外 ASCII 字符——其默认值为 `'/'`。

- 可选的 *encoding* 和 *errors* 参数
    指定如何处理非 ASCII 字符，如 `str.encode()` 方法所接受的那样。尽管这些参数在函数签名中默认为 `None`，但在处理 `str` 输入时，*encoding* 实际上默认为 `'utf-8'`，*errors* 默认为 `'strict'`，这意味着不支持的字符会引发 `UnicodeEncodeError`。如果 *string* 是 `bytes`，则不得提供 *encoding* 和 *errors*，否则会引发 `TypeError`。

注意
```py
quote(string, safe, encoding, errors)
# 等价于
quote_from_bytes(string.encode(encoding, errors), safe)
```

示例：
```py
quote('/El Niño/') # 产生 `'/El%20Ni%C3%B1o/'`
```

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

---

### http.server --- HTTP 服务器

https://docs.python.org/zh-cn/3.14/library/http.server.html

#### 命令行接口

```sh
python -m http.server [OPTIONS] [port]
```

选项
- `port`
    服务器默认监听 8000 端口

- `-p, --protocol <version>`
    指定服务器所采用的 HTTP 版本。 在默认情况下，服务器会采用 HTTP/1.0
