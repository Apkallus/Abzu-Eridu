https://requests.readthedocs.io/en/latest/api/#request-sessions

## 请求会话

### class `requests.Session`

Requests 会话。

提供 `cookie` 持久化、连接池和配置。

基本用法：

```pycon
>>> import requests
>>> s = requests.Session()
>>> s.get('https://httpbin.org/get')
<Response [200]>
```

或作为上下文管理器：

```pycon
>>> with requests.Session() as s:
...     s.get('https://httpbin.org/get')
<Response [200]>
```

#### `auth`

```py
auth: _t.AuthType
```

默认附加到 `Request` 的认证元组或对象。

#### `cert`

```py
cert: _t.CertType
```

SSL 客户端证书默认值；如果为字符串，则为 SSL 客户端证书文件（`.pem`）的路径。如果为元组，则为 (`'cert'`, `'key'`) 对。

#### `close()`

```py
close() → None
```

关闭所有适配器，从而关闭会话。

#### `cookies`

```py
cookies: RequestsCookieJar
```

包含此会话上当前设置的所有未过期 cookie 的 `CookieJar`。默认是 `RequestsCookieJar`，但也可以是任何其他 `cookielib.CookieJar` 兼容对象。

#### `delete()`

```py
delete(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

发送 DELETE 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `get()`

```py
get(url: _t.UriType, params: _t.ParamsType = None, **kwargs: Unpack[_t.GetKwargs]) → Response
```

发送 GET 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `params`  
    （可选）要在 `Request` 的查询字符串中发送的字典、元组列表或字节。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `get_adapter()`

```py
get_adapter(url: str) → BaseAdapter
```

返回给定 URL 的适当连接适配器。

- 返回类型  
    `requests.adapters.BaseAdapter`

#### `get_redirect_target()`

```py
get_redirect_target(resp: Response) → str | None
```

接收一个 `Response`。返回重定向 URI 或 `None`。

#### `head()`

```py
head(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

发送 HEAD 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `headers`

```py
headers: CaseInsensitiveDict[str]
```

一个大小写不敏感的标头字典，其中的标头会随从此 `Session` 发送的每个 `Request` 一起发送。

#### `hooks`

```py
hooks: dict[str, list[_t.HookType]]
```

事件处理钩子。

#### `max_redirects`

```py
max_redirects: int
```

允许的最大重定向次数。如果请求超过此限制，会引发 `TooManyRedirects` 异常。默认值为 `requests.models.DEFAULT_REDIRECT_LIMIT`，即 30。

#### `merge_environment_settings()`

```py
merge_environment_settings(url: str, proxies: dict[str, str] | None, stream: bool | None, verify: _t.VerifyType | None, cert: _t.CertType) → dict[str, Any]
```

检查环境并将其与某些设置合并。

- 返回类型  
    `dict`

#### `mount()`

```py
mount(prefix: str, adapter: BaseAdapter) → None
```

将连接适配器注册到前缀。

适配器按前缀长度降序排序。

#### `options()`

```py
options(url: _t.UriType, **kwargs: Unpack[_t.RequestKwargs]) → Response
```

发送 OPTIONS 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `params`

```py
params: MutableMapping[str, Any]
```

要附加到每个 `Request` 的查询字符串数据字典。字典值可以是列表，以表示多值查询参数。

#### `patch()`

```py
patch(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) → Response
```

发送 PATCH 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `data`  
    （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `post()`

```py
post(url: _t.UriType, data: _t.DataType = None, json: _t.JsonType = None, **kwargs: Unpack[_t.PostKwargs]) → Response
```

发送 POST 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `data`  
    （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。

- `json`  
    （可选）要在 `Request` 正文中发送的 json。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `prepare_request()`

```py
prepare_request(request: Request) → PreparedRequest
```

构造一个用于传输的 `PreparedRequest` 并返回它。`PreparedRequest` 的设置合并自 `Request` 实例和 `Session` 的设置。

- `request`  
    要使用此会话的设置进行准备的 `Request` 实例。

- 返回类型  
    `requests.PreparedRequest`

#### `proxies`

```py
proxies: dict[str, str]
```

将协议或协议和主机映射到代理 URL 的字典（例如 `{‘http’: ‘foo.bar:3128’, ‘http://host.name’: ‘foo.bar:4012’}`），用于每个 `Request`。

#### `put()`

```py
put(url: _t.UriType, data: _t.DataType = None, **kwargs: Unpack[_t.DataKwargs]) → Response
```

发送 PUT 请求。返回 `Response` 对象。

- `url`  
    新 `Request` 对象的 URL。

- `data`  
    （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。

- `**kwargs`  
    `request` 接受的可选参数。

- 返回类型  
    `requests.Response`

#### `rebuild_auth()`

```py
rebuild_auth(prepared_request: PreparedRequest, response: Response) → None
```

当发生重定向时，我们可能希望从请求中移除认证以避免泄露凭据。此方法会智能地移除并尽可能重新应用认证，以避免凭据丢失。

#### `rebuild_method()`

```py
rebuild_method(prepared_request: PreparedRequest, response: Response) → None
```

当发生重定向时，我们可能希望根据某些规范或浏览器行为更改请求的方法。

#### `rebuild_proxies()`

```py
rebuild_proxies(prepared_request: PreparedRequest, proxies: dict[str, str] | None) → dict[str, str]
```

此方法通过考虑环境变量重新评估代理配置。如果我们被重定向到 `NO_PROXY` 覆盖的 URL，则移除代理配置。否则，为此 URL 设置缺失的代理键（以防它们被先前的重定向移除）。

此方法还会在必要时替换 `Proxy-Authorization` 标头。

- 返回类型  
    `dict`

#### `request()`

```py
request(method: str, url: _t.UriType, params: _t.ParamsType = None, data: _t.DataType = None, headers: _t.HeadersType = None, cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, files: _t.FilesType = None, auth: _t.AuthType = None, timeout: _t.TimeoutType = None, allow_redirects: bool = True, proxies: dict[str, str] | None = None, hooks: _t.HooksInputType | None = None, stream: bool | None = None, verify: _t.VerifyType | None = None, cert: _t.CertType = None, json: _t.JsonType = None) → Response
```

构造一个 `Request`，准备并发送它。返回 `Response` 对象。

- `method`  
    新 `Request` 对象的方法。

- `url`  
    新 `Request` 对象的 URL。

- `params`  
    （可选）要在 `Request` 的查询字符串中发送的字典或字节。

- `data`  
    （可选）要在 `Request` 正文中发送的字典、元组列表、字节或类文件对象。

- `json`  
    （可选）要在 `Request` 正文中发送的 json。

- `headers`  
    （可选）随 `Request` 一起发送的 HTTP 标头字典。

- `cookies`  
    （可选）随 `Request` 一起发送的字典或 `CookieJar` 对象。

- `files`  
    （可选）用于多部分编码上传的 `'filename': file-like-objects` 字典。

- `auth`  
    （可选）认证元组或可调用对象，用于启用基本/摘要/自定义 HTTP 认证。

- `timeout`（`float` 或 `tuple`）  
    （可选）等待服务器发送数据的秒数，浮点数，或（连接超时、读取超时）元组。

- `allow_redirects`（`bool`）  
    （可选）默认设置为 `True`。

- `proxies`  
    （可选）将协议或协议和主机名映射到代理 URL 的字典。

- `hooks`  
    （可选）将钩子名称映射到一个事件或事件列表的字典，事件必须可调用。

- `stream`  
    （可选）是否立即下载响应内容。默认为 `False`。

- `verify`  
    （可选）可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是所要使用的 CA 证书包的路径。默认值为 `True`。当设置为 `False` 时，requests 将接受服务器提供的任何 TLS 证书，并忽略主机名不匹配和/或过期证书，这会使你的应用程序容易受到中间人（MitM）攻击。在本地开发或测试期间，将 `verify` 设置为 `False` 可能有用。

- `cert`  
    （可选）如果为字符串，则为 SSL 客户端证书文件（`.pem`）的路径。如果为元组，则为 (`'cert'`, `'key'`) 对。

- 返回类型  
    `requests.Response`

#### `resolve_redirects()`

```py
resolve_redirects(resp: Response, req: PreparedRequest, stream: bool = False, timeout: _t.TimeoutType = None, verify: _t.VerifyType = True, cert: _t.CertType = None, proxies: dict[str, str] | None = None, yield_requests: bool = False, **adapter_kwargs: Any) → Generator[Response, None, None]
```

接收一个 `Response`。返回 `Response` 或 `Request` 的生成器。

#### `send()`

```py
send(request: PreparedRequest, **kwargs: Any) → Response
```

发送给定的 `PreparedRequest`。

- 返回类型  
    `requests.Response`

#### `should_strip_auth()`

```py
should_strip_auth(old_url: str, new_url: str) → bool
```

决定在重定向时是否应移除 `Authorization` 标头。

#### `stream`

```py
stream: bool
```

流式响应内容默认值。

#### `trust_env`

```py
trust_env: bool
```

信任环境设置，用于代理配置、默认认证及类似功能。

#### `verify`

```py
verify: _t.VerifyType
```

SSL 验证默认值。默认为 `True`，要求 requests 验证远端 TLS 证书。如果 `verify` 设置为 `False`，requests 将接受服务器提供的任何 TLS 证书，并忽略主机名不匹配和/或过期证书，这会使你的应用程序容易受到中间人（MitM）攻击。仅在测试时将其设置为 `False`。如果 `verify` 设置为字符串，则它必须是用于验证 TLS 证书的 CA 证书包文件的路径。