<https://requests.readthedocs.io/en/latest/>

# requests —— Python HTTP 库

```python
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"type":"User"...'
>>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```

查看[没有 Requests 的类似代码](https://gist.github.com/973705)。

发送 HTTP/1.1 请求。无需手动向 URL 添加查询字符串，也无需对 POST 数据进行表单编码。得益于 [urllib3](https://github.com/urllib3/urllib3)，Keep-alive 和 HTTP 连接池 100% 自动。

## 备受喜爱的特性

Requests 已为当今的 Web 做好准备。

- Keep-Alive 与连接池
- 国际化域名和 URL
- 带 Cookie 持久化的会话
- 浏览器风格的 SSL 验证
- 自动内容解码
- 基本/摘要认证
- 优雅的键/值 Cookie
- 自动解压缩
- Unicode 响应体
- HTTP(S) 代理支持
- 多部分文件上传
- 流式下载
- 连接超时
- 分块请求
- `.netrc` 支持

Requests 官方支持 Python 3.10+，并在 PyPy 上运行良好。

--- 

https://requests.readthedocs.io/en/latest/api/

## 主要接口

Requests 的所有功能都可以通过以下 7 个方法访问。它们都返回一个 `Response` 对象的实例。

```python
requests.request(method: str, url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

构造并发送一个 `Request`。

**参数：**
- **method**
    新 `Request` 对象的方法：`GET`、`OPTIONS`、`HEAD`、`POST`、`PUT`、`PATCH` 或 `DELETE`。
- **url**
    新 `Request` 对象的 URL。
- **params**（可选）
    要在 `Request` 的查询字符串中发送的字典、元组列表或字节。
- **data**（可选）
    要在 `Request` 的正文中发送的字典、元组列表、字节或类文件对象。
- **json**（可选）
    要在 `Request` 的正文中发送的可 JSON 序列化的 Python 对象。
- **headers**（可选）
    随 `Request` 发送的 HTTP 头字典。
- **cookies**（可选）
    随 `Request` 发送的字典或 CookieJar 对象。
- **files**（可选）
    用于多部分编码上传的 `'name': file-like-objects`（或 `{'name': file-tuple}`）字典。`file-tuple` 可以是 2 元组 `('filename', fileobj)`、3 元组 `('filename', fileobj, 'content_type')` 或 4 元组 `('filename', fileobj, 'content_type', custom_headers)`，其中 `'content_type'` 是定义给定文件内容类型的字符串，`custom_headers` 是包含要为该文件添加的附加头的类字典对象。
- **auth**（可选）
    用于启用基本/摘要/自定义 HTTP 认证的认证元组。
- **timeout**（`float` 或 `tuple`）（可选）
    在放弃之前等待服务器发送数据的秒数，可以是浮点数，也可以是（连接超时，读取超时）元组。
- **allow_redirects**（`bool`）（可选）
    布尔值。启用/禁用 GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD 重定向。默认为 `True`。
- **proxies**（可选）
    将协议映射到代理 URL 的字典。
- **verify**（可选）
    可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是 CA 捆绑包的路径。默认为 `True`。
- **stream**（可选）
    如果为 `False`，响应内容将立即下载。
- **cert**（可选）
    如果是字符串，则为 SSL 客户端证书文件（.pem）的路径。如果是元组，则为（'cert', 'key'）对。

**返回：**
- `Response` 对象

**返回类型：**
- `requests.Response`

用法：

```python
>>> import requests
>>> res = requests.request('GET', 'https://httpbin.org/get')
>>> res
<Response [200]>
```

### requests.head

```python
requests.head(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

发送一个 HEAD 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- ****kwargs**
    `request` 接受的可选参数。如果未提供 `allow_redirects`，它将被设置为 `False`（与默认的 `request` 行为相反）。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

### requests.get

```python
requests.get(url: _t.UriType, params: _t.ParamsType = None, **kwargs: Unpack[_t.GetKwargs]) → Response
```

发送一个 GET 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- **params**（可选）
    要在 `Request` 的查询字符串中发送的字典、元组列表或字节。
- ****kwargs**
    `request` 接受的可选参数。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

### requests.post

```python
requests.post(url: _t.UriType, data: _t.DataType = None, json: _t.JsonType = None, **kwargs: Unpack[_t.PostKwargs]) → Response
```

发送一个 POST 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- **data**（可选）
    要在 `Request` 的正文中发送的字典、元组列表、字节或类文件对象。
- **json**（可选）
    要在 `Request` 的正文中发送的可 JSON 序列化的 Python 对象。
- ****kwargs**
    `request` 接受的可选参数。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

### requests.put

```python
requests.put(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) → Response
```

发送一个 PUT 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- **data**（可选）
    要在 `Request` 的正文中发送的字典、元组列表、字节或类文件对象。
- **json**（可选）
    要在 `Request` 的正文中发送的可 JSON 序列化的 Python 对象。
- ****kwargs**
    `request` 接受的可选参数。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

### requests.patch

```python
requests.patch(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) → Response
```

发送一个 PATCH 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- **data**（可选）
    要在 `Request` 的正文中发送的字典、元组列表、字节或类文件对象。
- **json**（可选）
    要在 `Request` 的正文中发送的可 JSON 序列化的 Python 对象。
- ****kwargs**
    `request` 接受的可选参数。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

### requests.delete

```python
requests.delete(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

发送一个 DELETE 请求。

**参数：**

- **url**
    新 `Request` 对象的 URL。
- ****kwargs**
    `request` 接受的可选参数。

**返回：**

`Response` 对象

**返回类型：**

`requests.Response`

## Request Sessions —— class requests.Session

https://requests.readthedocs.io/en/latest/api/#requests.Session

一个 Requests 会话。

提供 cookie 持久化、连接池和配置。

基本用法：

```python
>>> import requests
>>> s = requests.Session()
>>> s.get('https://httpbin.org/get')
<Response [200]>
```

或作为上下文管理器：

```python
>>> with requests.Session() as s:
...     s.get('https://httpbin.org/get')
<Response [200]>
```

### 属性

- `auth: _t.AuthType`  
  默认认证元组或对象，附加到 `Request`。

- `cert: _t.CertType`  
  SSL 客户端证书默认值。如果是字符串，则为 SSL 客户端证书文件（`.pem`）的路径。如果是元组，则为 `('cert', 'key')` 对。

- `cookies: RequestsCookieJar`  
  一个 `CookieJar`，包含当前在此会话上设置的所有未过期 cookie。默认是 `RequestsCookieJar`，但也可以是任何其他与 `cookielib.CookieJar` 兼容的对象。

- `headers: CaseInsensitiveDict[str]`  
  一个大小写不敏感的头部字典，将在此 `Session` 发送的每个 `Request` 上发送。

- `hooks: dict[str, list[_t.HookType]]`  
  事件处理钩子。

- `max_redirects: int`  
  允许的最大重定向次数。如果请求超过此限制，将引发 `TooManyRedirects` 异常。默认值为 `requests.models.DEFAULT_REDIRECT_LIMIT`，即 30。

- `params: MutableMapping[str, Any]`  
  要附加到每个 `Request` 的查询字符串数据字典。字典值可以是列表，用于表示多值查询参数。

- `proxies: dict[str, str]`  
  将协议或协议和主机映射到代理 URL 的字典（例如 `{'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}`），用于每个 `Request`。

- `stream: bool`  
  流式传输响应内容的默认值。

- `trust_env: bool`  
  信任环境设置，用于代理配置、默认认证及类似功能。

- `verify: _t.VerifyType`  
  SSL 验证默认值。默认是 `True`，要求 requests 验证远端的 TLS 证书。如果将 `verify` 设置为 `False`，requests 将接受服务器提供的任何 TLS 证书，并忽略主机名不匹配和/或过期证书，这会使你的应用程序容易受到中间人（MitM）攻击。仅在测试时将其设置为 `False`。如果 `verify` 设置为字符串，则它必须是将用于验证 TLS 证书的 CA 捆绑包文件的路径。

### 方法

#### `close`

```python
close() -> None
```

关闭所有适配器，从而关闭会话。

#### `delete`

```python
delete(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) -> Response
```

发送 DELETE 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `get`

```python
get(url: _t.UriType, params: _t.ParamsType = None, **kwargs: Unpack[_t.GetKwargs]) -> Response
```

发送 GET 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `params` – （可选）要在 `Request` 的查询字符串中发送的字典、元组列表或字节。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `get_adapter`

```python
get_adapter(url: str) -> BaseAdapter
```

返回给定 URL 的适当连接适配器。

返回类型：`requests.adapters.BaseAdapter`

#### `get_redirect_target`

```python
get_redirect_target(resp: Response) -> str | None
```

接收一个 `Response`。返回重定向 URI 或 `None`。

#### `head`

```python
head(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) -> Response
```

发送 HEAD 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `merge_environment_settings`

```python
merge_environment_settings(
    url: str,
    proxies: dict[str, str] | None,
    stream: bool | None,
    verify: _t.VerifyType | None,
    cert: _t.CertType
) -> dict[str, Any]
```

检查环境并将其与某些设置合并。

返回类型：`dict`

#### `mount`

```python
mount(prefix: str, adapter: BaseAdapter) -> None
```

将连接适配器注册到前缀。

适配器按前缀长度降序排序。

#### `options`

```python
options(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) -> Response
```

发送 OPTIONS 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `patch`

```python
patch(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) -> Response
```

发送 PATCH 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `data` – （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `post`

```python
post(
    url: _t.UriType,
    data: _t.DataType = None,
    json: _t.JsonType = None,
    **kwargs: Unpack[_t.PostKwargs]
) -> Response
```

发送 POST 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `data` – （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。
- `json` – （可选）要在 `Request` 正文中发送的 json。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `prepare_request`

```python
prepare_request(request: Request) -> PreparedRequest
```

构造用于传输的 `PreparedRequest` 并返回它。`PreparedRequest` 合并了 `Request` 实例和 `Session` 的设置。

参数：
- `request` – 要使用此会话设置准备的 `Request` 实例。

返回类型：`requests.PreparedRequest`

#### `put`

```python
put(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) -> Response
```

发送 PUT 请求。返回 `Response` 对象。

参数：
- `url` – 新 `Request` 对象的 URL。
- `data` – （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。
- `**kwargs` – `request` 接受的可选参数。

返回类型：`requests.Response`

#### `rebuild_auth`

```python
rebuild_auth(prepared_request: PreparedRequest, response: Response) -> None
```

当发生重定向时，我们可能希望从请求中剥离认证信息，以避免泄露凭据。此方法会尽可能智能地移除并重新应用认证信息，以避免凭据丢失。

#### `rebuild_method`

```python
rebuild_method(prepared_request: PreparedRequest, response: Response) -> None
```

当发生重定向时，我们可能希望根据某些规范或浏览器行为更改请求方法。

#### `rebuild_proxies`

```python
rebuild_proxies(
    prepared_request: PreparedRequest,
    proxies: dict[str, str] | None
) -> dict[str, str]
```

此方法通过考虑环境变量重新评估代理配置。如果我们被重定向到由 `NO_PROXY` 覆盖的 URL，则剥离代理配置。否则，我们为此 URL 设置缺失的代理键（以防它们被先前的重定向剥离）。

此方法还会在必要时替换 `Proxy-Authorization` 头。

返回类型：`dict`

#### `request`

```python
request(
    method: str,
    url: _t.UriType,
    params: _t.ParamsType = None,
    data: _t.DataType = None,
    headers: _t.HeadersType = None,
    cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None,
    files: _t.FilesType = None,
    auth: _t.AuthType = None,
    timeout: _t.TimeoutType = None,
    allow_redirects: bool = True,
    proxies: dict[str, str] | None = None,
    hooks: _t.HooksInputType | None = None,
    stream: bool | None = None,
    verify: _t.VerifyType | None = None,
    cert: _t.CertType = None,
    json: _t.JsonType = None
) -> Response
```

构造一个 `Request`，准备并发送它。返回 `Response` 对象。

参数：
- `method` – 新 `Request` 对象的方法。
- `url` – 新 `Request` 对象的 URL。
- `params` – （可选）要在 `Request` 的查询字符串中发送的字典或字节。
- `data` – （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。
- `json` – （可选）要在 `Request` 正文中发送的 json。
- `headers` – （可选）随 `Request` 发送的 HTTP 头字典。
- `cookies` – （可选）随 `Request` 发送的字典或 `CookieJar` 对象。
- `files` – （可选）用于 multipart 编码上传的 `'filename': file-like-objects` 字典。
- `auth` – （可选）启用 Basic/Digest/Custom HTTP Auth 的认证元组或可调用对象。
- `timeout` – （可选）在放弃之前等待服务器发送数据的秒数，可以是浮点数，或 `(connect timeout, read timeout)` 元组。
- `allow_redirects` – （可选）默认设置为 `True`。
- `proxies` – （可选）将协议或协议和主机名映射到代理 URL 的字典。
- `hooks` – （可选）将钩子名称映射到一个事件或事件列表的字典，事件必须可调用。
- `stream` – （可选）是否立即下载响应内容。默认为 `False`。
- `verify` – （可选）可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是使用的 CA 捆绑包路径。默认为 `True`。当设置为 `False` 时，requests 将接受服务器提供的任何 TLS 证书，并忽略主机名不匹配和/或过期证书，这会使你的应用程序容易受到中间人（MitM）攻击。在本地开发或测试期间，将 `verify` 设置为 `False` 可能有用。
- `cert` – （可选）如果是字符串，则为 SSL 客户端证书文件（`.pem`）的路径。如果是元组，则为 `('cert', 'key')` 对。

返回类型：`requests.Response`

#### `resolve_redirects`

```python
resolve_redirects(
    resp: Response,
    req: PreparedRequest,
    stream: bool = False,
    timeout: _t.TimeoutType = None,
    verify: _t.VerifyType = True,
    cert: _t.CertType = None,
    proxies: dict[str, str] | None = None,
    yield_requests: bool = False,
    **adapter_kwargs: Any
) -> Generator[Response, None, None]
```

接收一个 `Response`。返回 `Responses` 或 `Requests` 的生成器。

#### `send`

```python
send(request: PreparedRequest, **kwargs: Any) -> Response
```

发送给定的 `PreparedRequest`。

返回类型：`requests.Response`

#### `should_strip_auth`

```python
should_strip_auth(old_url: str, new_url: str) -> bool
```

决定重定向时是否应移除 `Authorization` 头。

## Lower-Level Classes

https://requests.readthedocs.io/en/latest/api/#lower-level-classes

### ♾️ class requests.Request —— 设置请求字段

```python
class requests.Request(
    method: str | None = None, 
    url: _t.UriType | None = None, 
    headers: _t.HeadersType = None, 
    files: _t.FilesType = None, 
    data: _t.DataType = None, 
    params: _t.ParamsType = None, 
    auth: _t.AuthType = None, 
    cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, 
    hooks: _t.HooksInputType | None = None, 
    json: _t.JsonType = None
)
```

用户创建的 `Request` 对象。

用于准备发送到服务器的 `PreparedRequest`。

用法：

```python
>>> import requests
# 设置请求字段
>>> req = requests.Request('GET', 'https://httpbin.org/get')
# 导出为字节
>>> req.prepare()
<PreparedRequest [GET]>
# 之后发送请求字节
```

**参数：**

- **method** – 要使用的 HTTP 方法。
- **url** – 要发送的 URL。
- **headers** – 要发送的标头字典。
- **files** – 要用于多部分上传的 `{filename: fileobject}` 文件字典。
- **data** – 要附加到请求的正文。如果提供了字典或元组列表 `[(key, value)]`，将进行表单编码。
- **json** – 要附加到请求正文的 JSON 或字典（如果未指定 files 或 data）。
- **params** – 要附加到 URL 的 URL 参数。如果提供了字典或元组列表 `[(key, value)]`，将进行表单编码。
- **auth** – 认证处理程序或 (user, pass) 元组。
- **cookies** – 要附加到此请求的 cookie 字典或 CookieJar。
- **hooks** – 回调钩子字典，供内部使用。

#### deregister_hook

```python
deregister_hook(event: str, hook: Callable[[Response], Any]) → bool
```

注销之前注册的钩子。如果钩子存在则返回 `True`，否则返回 `False`。

#### prepare

```python
prepare() → PreparedRequest
```

构造一个用于传输的 `PreparedRequest` 并返回它。

```python
register_hook(event: str, hook: Iterable[Callable[[Response], Any]] | Callable[[Response], Any]) → None
```

正确地注册一个钩子。

### ♾️ class requests.Response —— 响应对象

https://requests.readthedocs.io/en/latest/api/#requests.Response

`Response` 对象，包含服务器对 HTTP 请求的响应。

> 获取数据，并打印调试信息

#### ♾️ 属性

- `property apparent_encoding: str | None`  
  表观编码，由 `charset_normalizer` 或 `chardet` 库提供。

- `property content: bytes`  
  响应的内容，以字节为单位。
  > `b''` 原始字节

- `cookies: RequestsCookieJar`  
  服务器发回的 Cookies 的 `CookieJar`。

- `elapsed: datetime.timedelta`  
  从发送请求到响应到达之间经过的时间（以 `timedelta` 表示）。此属性专门测量从发送请求的第一个字节到完成解析头部所花费的时间。因此它不受消费响应内容或 `stream` 关键字参数值的影响。

- `encoding: str | None`  
  访问 `r.text` 时用于解码的编码。

- `headers: CaseInsensitiveDict[str]`  
  响应头的大小写不敏感字典。例如，`headers['content-encoding']` 将返回 `'Content-Encoding'` 响应头的值。

- `history: list[Response]`  
  请求历史中的 `Response` 对象列表。任何重定向响应都会出现在这里。列表按从最旧到最新的请求排序。

- `property is_redirect: bool`  
  如果此 `Response` 是一个格式良好的 HTTP 重定向，并且可以被自动处理（由 `Session.resolve_redirects` 处理），则为 `True`。

- `property links: dict[str, dict[str, str]]`  
  返回响应中解析后的头部链接（如果有）。

- `property next: PreparedRequest | None`  
  返回重定向链中下一个请求的 `PreparedRequest`，如果存在的话。

- `property ok: bool`  
  如果 `status_code` 小于 400，则返回 `True`，否则返回 `False`。

  此属性检查响应的状态码是否在 400 到 600 之间，以判断是客户端错误还是服务器错误。如果状态码在 200 到 400 之间，则返回 `True`。这**不是**检查响应码是否为 `200 OK`。

- `raw: Any`  
  响应的类文件对象表示（用于高级用法）。使用 `raw` 要求请求上设置了 `stream=True`。此要求不适用于 Requests 内部使用。

- `reason: str`  
  响应 HTTP 状态的文本原因，例如 “Not Found” 或 “OK”。

- `request: PreparedRequest`  
  此响应对应的 `PreparedRequest` 对象。

- `status_code: int`  
  响应 HTTP 状态的整数代码，例如 404 或 200。

- `property text: str`  
  响应的内容，以 unicode 表示。
  > 自动解码

  如果 `Response.encoding` 为 `None`，将使用 `charset_normalizer` 或 `chardet` 猜测编码。

  响应内容的编码仅基于 HTTP 头部确定，严格遵循 RFC 2616。如果你可以利用非 HTTP 知识来更好地猜测编码，应在访问此属性之前适当地设置 `r.encoding`。

- `url: str`  
  响应的最终 URL 位置。

#### 方法

##### `close`

```python
close() -> None
```

将连接释放回池。一旦调用此方法，就不能再次访问底层 `raw` 对象。

*注意：通常不需要显式调用。*

##### `iter_content`

```python
iter_content(chunk_size: int | None = 1, decode_unicode: Literal[False] = False) -> Iterator[bytes]
iter_content(chunk_size: int | None = 1, *, decode_unicode: Literal[True]) -> Iterator[str | bytes]
```

迭代响应数据。当请求上设置了 `stream=True` 时，这可以避免将大型响应的内容一次性读入内存。`chunk_size` 是应读入内存的字节数。由于可能进行解码，这不一定是返回的每个项的长度。

`chunk_size` 必须是 `int` 或 `None`。`None` 值的行为取决于 `stream` 的值。`stream=True` 将按数据到达时的块大小读取数据。如果 `stream=False`，数据将作为单个块返回。

如果 `decode_unicode` 为 `True`，将使用响应中的编码信息解码内容。如果没有可用的编码信息，将返回字节。可以通过在响应上手动设置 `encoding` 来绕过此行为。

##### `iter_lines`

```python
iter_lines(chunk_size: int = ITER_CHUNK_SIZE, decode_unicode: Literal[False] = False, delimiter: bytes | None = None) -> Iterator[bytes]
iter_lines(chunk_size: int = ITER_CHUNK_SIZE, *, decode_unicode: Literal[True], delimiter: str | bytes | None = None) -> Iterator[str | bytes]
```

一次一行地迭代响应数据。当请求上设置了 `stream=True` 时，这可以避免将大型响应的内容一次性读入内存。

`decode_unicode` 参数的工作方式与 `iter_content` 中相同，并具有相同的注意事项。

注意：此方法不是可重入安全的。

##### `json`

```python
json(**kwargs: Any) -> Any
```

将 JSON 响应体（如果有）解码为 Python 对象。

这可能返回字典、列表等，具体取决于响应中的内容。

参数：
- `**kwargs` – `json.loads` 接受的可选参数。

引发：
- `requests.exceptions.JSONDecodeError` – 如果响应体不包含有效的 json。

##### `raise_for_status`

```python
raise_for_status() -> None
```

如果发生错误，则引发 `HTTPError`。

## Lower-Lower-Level Classes

https://requests.readthedocs.io/en/latest/api/#lower-lower-level-classes


### ♾️ class requests.PreparedRequest —— 将发送的请求字节

完全可变的 `PreparedRequest` 对象，包含将发送到服务器的确切*字节*。

> 调试时访问属性以打印请求各字段，方法目前未使用

实例由 `Request` 对象生成，不应手动实例化；这样做可能产生不良影响。

用法：

```python
>>> import requests
>>> req = requests.Request('GET', 'https://httpbin.org/get')
>>> r = req.prepare()
>>> r
<PreparedRequest [GET]>

>>> s = requests.Session()
>>> s.send(r)
<Response [200]>
```

#### ♾️ 属性

- `body: _t.BodyType`  
  发送到服务器的请求体。
  > `b''` 原始字节

- `headers: CaseInsensitiveDict[str | bytes]`  
  HTTP 头字典。

- `hooks: dict[str, list[_t.HookType]]`  
  回调钩子字典，供内部使用。

- `method: str | None`  
  发送到服务器的 HTTP 动词。

- `property path_url: str`  
  构建要使用的路径 URL。

- `url: str | None`  
  要将请求发送到的 HTTP URL。

#### 方法

##### `deregister_hook`

```python
deregister_hook(event: str, hook: Callable[[Response], Any]) -> bool
```

注销先前注册的钩子。如果钩子存在，则返回 `True`，否则返回 `False`。

##### `prepare`

```python
prepare(
    method: str | None = None,
    url: _t.UriType | None = None,
    headers: Mapping[str, str | bytes] | None = None,
    files: _t.FilesType = None,
    data: _t.DataType = None,
    params: _t.ParamsType = None,
    auth: _t.AuthType = None,
    cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None,
    hooks: _t.HooksInputType | None = None,
    json: _t.JsonType = None
) -> None
```

使用给定参数准备整个请求。

##### `prepare_auth`

```python
prepare_auth(auth: _t.AuthType, url: _t.UriType = '') -> None
```

准备给定的 HTTP 认证数据。

##### `prepare_body`

```python
prepare_body(data: _t.DataType, files: _t.FilesType, json: _t.JsonType = None) -> None
```

准备给定的 HTTP 正文数据。

##### `prepare_content_length`

```python
prepare_content_length(body: _t.BodyType) -> None
```

根据请求方法和正文准备 `Content-Length` 头。

##### `prepare_cookies`

```python
prepare_cookies(cookies: RequestsCookieJar | CookieJar | dict[str, str] | None) -> None
```

准备给定的 HTTP cookie 数据。

此函数最终使用 `cookielib` 从给定 cookie 生成 `Cookie` 头。由于 `cookielib` 的设计，如果该头已存在，则不会重新生成，这意味着该函数在 `PreparedRequest` 对象的生命周期内只能调用一次。任何后续对 `prepare_cookies` 的调用都不会产生实际效果，除非事先移除了 `Cookie` 头。

##### `prepare_headers`

```python
prepare_headers(headers: Mapping[str, str | bytes] | None) -> None
```

准备给定的 HTTP 头。

##### `prepare_hooks`

```python
prepare_hooks(hooks: Mapping[str, Iterable[Callable[[Response], Any]] | Callable[[Response], Any]] | None) -> None
```

准备给定的钩子。

##### `prepare_method`

```python
prepare_method(method: str | None) -> None
```

准备给定的 HTTP 方法。

##### `prepare_url`

```python
prepare_url(url: _t.UriType, params: _t.ParamsType) -> None
```

准备给定的 HTTP URL。

##### `register_hook`

```python
register_hook(event: str, hook: Iterable[Callable[[Response], Any]] | Callable[[Response], Any]) -> None
```

正确注册钩子。