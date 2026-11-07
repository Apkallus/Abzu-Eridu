https://requests.readthedocs.io/en/latest/api/#lower-lower-level-classes

## 更低层级类

### class requests.PreparedRequest

完全可变的 `PreparedRequest` 对象，包含将发送到服务器的确切字节。

实例由 `Request` 对象生成，不应手动实例化；否则可能产生不良影响。

用法：

```pycon
>>> import requests
>>> req = requests.Request('GET', 'https://httpbin.org/get')
>>> r = req.prepare()
>>> r
<PreparedRequest [GET]>

>>> s = requests.Session()
>>> s.send(r)
<Response [200]>
```

- `body: _t.BodyType`  
    要发送到服务器的请求体。

- 
    ```py
    deregister_hook(event: str, hook: Callable[[Response], Any]) → bool
    ```
    注销先前注册的钩子。如果钩子存在则返回 `True`，否则返回 `False`。

- `headers: CaseInsensitiveDict[str | bytes]`  
    HTTP 头字典。

- `hooks: dict[str, list[_t.HookType]]`  
    内部使用的回调钩子字典。

- `method: str | None`  
    要发送到服务器的 HTTP 动词。

- `path_url: str`  
    构建要使用的路径 URL。

- 
    ```py
    prepare(method: str | None = None, url: _t.UriType | None = None, headers: Mapping[str, str | bytes] | None = None, files: _t.FilesType = None, data: _t.DataType = None, params: _t.ParamsType = None, auth: _t.AuthType = None, cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, hooks: _t.HooksInputType | None = None, json: _t.JsonType = None) → None
    ```
    使用给定参数准备整个请求。

- 
    ```py
    prepare_auth(auth: _t.AuthType, url: _t.UriType = '') → None
    ```
    准备给定的 HTTP 认证数据。

- 
    ```py
    prepare_body(data: _t.DataType, files: _t.FilesType, json: _t.JsonType = None) → None
    ```
    准备给定的 HTTP 正文数据。

- 
    ```py
    prepare_content_length(body: _t.BodyType) → None
    ```
    根据请求方法和正文准备 `Content-Length` 头。

- 
    ```py
    prepare_cookies(cookies: RequestsCookieJar | CookieJar | dict[str, str] | None) → None
    ```
    准备给定的 HTTP cookie 数据。

    此函数最终会使用 `cookielib` 从给定 cookies 生成一个 `Cookie` 头。由于 `cookielib` 的设计，如果该头已存在，则不会重新生成，这意味着此函数在 `PreparedRequest` 对象的生命周期内只能调用一次。任何后续对 `prepare_cookies` 的调用都不会产生实际效果，除非事先移除 “Cookie” 头。

- 
    ```py
    prepare_headers(headers: Mapping[str, str | bytes] | None) → None
    ```
    准备给定的 HTTP 头。

- 
    ```py
    prepare_hooks(hooks: Mapping[str, Iterable[Callable[[Response], Any]] | Callable[[Response], Any]] | None) → None
    ```
    准备给定的钩子。

- 
    ```py
    prepare_method(method: str | None) → None
    ```
    准备给定的 HTTP 方法。

- 
    ```py
    prepare_url(url: _t.UriType, params: _t.ParamsType) → None
    ```
    准备给定的 HTTP URL。

- 
    ```py
    register_hook(event: str, hook: Iterable[Callable[[Response], Any]] | Callable[[Response], Any]) → None
    ```
    正确注册一个钩子。

- `url: str | None`  
    要发送请求的 HTTP URL。

### class requests.adapters.BaseAdapter

基础传输适配器。

#### close() → None

清理适配器特定项。

#### send()

```py
send(request: PreparedRequest, stream: bool = False, timeout: _t.TimeoutType = None, verify: _t.VerifyType = True, cert: _t.CertType = None, proxies: dict[str, str] | None = None) → Response
```

发送 `PreparedRequest` 对象。返回 `Response` 对象。

参数：

- `request`  
    正在发送的 `PreparedRequest`。

- `stream`  
    （可选）是否流式传输请求内容。

- `timeout（float 或 tuple）`  
    （可选）等待服务器发送数据多久后放弃，以浮点数表示，或 `[连接超时, 读取超时]` 元组。

- `verify`  
    （可选）可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是要使用的 CA 包路径。

- `cert`  
    （可选）任何要信任的用户提供的 SSL 证书。

- `proxies`  
    （可选）要应用于请求的代理字典。

### class requests.adapters.HTTPAdapter()

```py
class HTTPAdapter(pool_connections: int = 10, pool_maxsize: int = 10, max_retries: int | Retry = 0, pool_block: bool = False)
```

urllib3 的内置 HTTP 适配器。

为 Requests 会话提供通用接口，通过实现传输适配器接口来联系 HTTP 和 HTTPS URL。此类通常由 `Session` 类在后台创建。

参数：

- `pool_connections`  
    要缓存的 urllib3 连接池数量。

- `pool_maxsize`  
    池中保存的最大连接数。

- `max_retries`  
    每个连接应尝试的最大重试次数。注意，这仅适用于失败的 DNS 查找、套接字连接和连接超时，从不适用于数据已到达服务器的请求。默认情况下，Requests 不会重试失败的连接。如果你需要对重试请求的条件进行细粒度控制，请导入 urllib3 的 `Retry` 类并传入。

- `pool_block`  
    连接池是否应阻塞等待连接。

用法：

```pycon
>>> import requests
>>> s = requests.Session()
>>> a = requests.adapters.HTTPAdapter(max_retries=3)
>>> s.mount('http://', a)
```

#### add_headers()

```py
add_headers(request: PreparedRequest, **kwargs: Any) → None
```

添加连接所需的任何头。自 v2.0 起，默认情况下此方法不执行任何操作，但保留给子类化 `HTTPAdapter` 的用户覆盖。

不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `request`  
    要向其中添加头的 `PreparedRequest`。

- `kwargs`  
    来自 `send()` 调用的关键字参数。

#### build_connection_pool_key_attributes()

```py
build_connection_pool_key_attributes(request: PreparedRequest, verify: _t.VerifyType, cert: _t.CertType = None) → tuple[dict[str, Any], dict[str, Any]]
```

构建 urllib3 用于返回连接的 `PoolKey` 属性。

此方法会查看 `PreparedRequest`、用户指定的 `verify` 值以及 `cert` 参数的值，以确定使用哪些 `PoolKey` 值从给定的 urllib3 连接池中选择连接。

与 SSL 相关的池键参数并未一致设置。截至撰写本文时，可使用以下规则确定该字典中可能包含哪些键：

- 如果 `verify` 为 `True`，将设置 `"ssl_context"`，并且它是默认的 Requests SSL Context
- 如果 `verify` 为 `False`，不会设置 `"ssl_context"`，但会设置 `"cert_reqs"`
- 如果 `verify` 是字符串（即用户指定的信任包），若该字符串不是 `os.path.isdir` 可识别的目录，则设置 `"ca_certs"`，否则设置 `"ca_cert_dir"`
- 如果指定了 `"cert"`，将始终设置 `"cert_file"`。如果 `"cert"` 是包含第二项的元组，则还会存在 `"key_file"`

要覆盖这些设置，可以子类化此类，调用此方法，并使用上述逻辑按需更改参数。例如，如果希望使用自定义的 [`ssl.SSLContext`](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.SSLContext)，则必须同时设置 `"ssl_context"`，并根据其他需求更改其他键以确保所需行为。

参数：

- `request（PreparedRequest）`  
    正在通过连接发送的 `PreparedRequest`。

- `verify`  
    可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是要使用的 CA 包路径。

- `cert`  
    （可选）任何用户提供的用于客户端认证（又称 mTLS）的 SSL 证书。这可以是字符串（即仅包含证书和密钥的文件的路径），也可以是长度为 2 的元组，包含证书文件路径和密钥文件路径。

返回：

一个包含两个字典的元组。第一个是 `PoolKey` 的“主机参数”部分，包括 `scheme`、`hostname` 和 `port`。第二个是 SSLContext 相关参数字典。

#### build_response()

```py
build_response(req: PreparedRequest, resp: Any) → Response
```

从 urllib3 响应构建 `Response` 对象。不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `req`  
    用于生成响应的 `PreparedRequest`。

- `resp`  
    urllib3 响应对象。

返回类型：`requests.Response`

#### cert_verify()

```py
cert_verify(conn: Any, url: str, verify: _t.VerifyType, cert: _t.CertType) → None
```

验证 SSL 证书。不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `conn`  
    与证书关联的 urllib3 连接对象。

- `url`  
    请求的 URL。

- `verify`  
    可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是要使用的 CA 包路径。

- `cert`  
    要验证的 SSL 证书。

#### close() → None

释放任何内部状态。

目前，这会关闭 `PoolManager` 和任何活动的 `ProxyManager`，从而关闭任何池化连接。

#### get_connection()

```py
get_connection(url: str, proxies: dict[str, str] | None = None) → HTTPConnectionPool
```

已弃用：对于使用 Requests>=2.32.2 的所有 `HTTPAdapter` 子类，用户应改用 `get_connection_with_tls_context`。

返回给定 URL 的 urllib3 连接。不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `url`  
    要连接的 URL。

- `proxies`  
    （可选）Requests 风格的代理字典，用于此请求。

返回类型：[urllib3.HTTPConnectionPool](https://urllib3.readthedocs.io/en/latest/reference/urllib3.connectionpool.html#urllib3.HTTPConnectionPool)

#### get_connection_with_tls_context()

```py
get_connection_with_tls_context(request: PreparedRequest, verify: _t.VerifyType, proxies: dict[str, str] | None = None, cert: _t.CertType = None) → HTTPConnectionPool
```

返回给定请求和 TLS 设置的 urllib3 连接。不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `request`  
    要通过连接发送的 `PreparedRequest` 对象。

- `verify`  
    可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是要使用的 CA 包路径。

- `proxies`  
    （可选）要应用于请求的代理字典。

- `cert`  
    （可选）任何用户提供的用于客户端认证（又称 mTLS）的 SSL 证书。

返回类型：[urllib3.HTTPConnectionPool](https://urllib3.readthedocs.io/en/latest/reference/urllib3.connectionpool.html#urllib3.HTTPConnectionPool)

#### init_poolmanager()

```py
init_poolmanager(connections: int, maxsize: int, block: bool = False, **pool_kwargs: Any) → None
```

初始化 urllib3 `PoolManager`。

不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `connections`  
    要缓存的 urllib3 连接池数量。

- `maxsize`  
    池中保存的最大连接数。

- `block`  
    没有空闲连接时是否阻塞。

- `pool_kwargs`  
    用于初始化 `PoolManager` 的额外关键字参数。

#### proxy_headers()

```py
proxy_headers(proxy: str) → dict[str, str]
```

返回要通过代理发送的任何请求所需添加的头的字典。此方法利用 urllib3 的魔法来确保它们被正确发送到代理，而不是在使用 `CONNECT` 时出现在隧道请求中。

不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `proxy`  
    用于此请求的代理 URL。

返回类型：`dict`

#### proxy_manager_for()

```py
proxy_manager_for(proxy: str, **proxy_kwargs: Any) → Any
```

返回给定代理的 urllib3 `ProxyManager`。

不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `proxy`  
    要为其返回 urllib3 `ProxyManager` 的代理。

- `proxy_kwargs`  
    用于配置 `ProxyManager` 的额外关键字参数。

返回：`ProxyManager`

返回类型：[urllib3.ProxyManager](https://urllib3.readthedocs.io/en/latest/reference/urllib3.poolmanager.html#urllib3.ProxyManager)

#### request_url()

```py
request_url(request: PreparedRequest, proxies: dict[str, str] | None) → str
```

获取发出最终请求时要使用的 URL。

如果消息通过 HTTP 代理发送，则必须使用完整 URL。否则，我们应仅使用 URL 的路径部分。

不应从用户代码中调用此方法，仅在子类化 `HTTPAdapter` 时暴露使用。

参数：

- `request`  
    正在发送的 `PreparedRequest`。

- `proxies`  
    方案或方案与主机到代理 URL 的字典。

返回类型：`str`

#### send()

```py
send(request: PreparedRequest, stream: bool = False, timeout: _t.TimeoutType = None, verify: _t.VerifyType = True, cert: _t.CertType = None, proxies: dict[str, str] | None = None) → Response
```

发送 `PreparedRequest` 对象。返回 `Response` 对象。

参数：

- `request`  
    正在发送的 `PreparedRequest`。

- `stream`  
    （可选）是否流式传输请求内容。

- `timeout（float 或 tuple 或 urllib3 Timeout 对象）`  
    （可选）等待服务器发送数据多久后放弃，以浮点数表示，或 `[连接超时, 读取超时]` 元组。

- `verify`  
    （可选）可以是布尔值，此时控制是否验证服务器的 TLS 证书；也可以是字符串，此时必须是要使用的 CA 包路径。

- `cert`  
    （可选）任何要信任的用户提供的 SSL 证书。

- `proxies`  
    （可选）要应用于请求的代理字典。

返回类型：`requests.Response`