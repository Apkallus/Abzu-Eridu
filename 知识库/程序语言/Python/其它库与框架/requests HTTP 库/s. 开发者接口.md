# 开发者接口

本部分文档涵盖 `Requests` 的所有接口。

## Lower-Level Classes

https://requests.readthedocs.io/en/latest/api/#lower-level-classes

### class requests.Request() —— 设置请求字段

```py
class requests.Request(method: str | None = None, url: _t.UriType | None = None, headers: _t.HeadersType = None, files: _t.FilesType = None, data: _t.DataType = None, params: _t.ParamsType = None, auth: _t.AuthType = None, cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, hooks: _t.HooksInputType | None = None, json: _t.JsonType = None)
```

用户创建的 [`Request`] 对象。

用于准备 [`PreparedRequest`]，并将其发送到服务器。


- `method`  
    HTTP 方法。

- `url`  
    要发送的 URL。

- `headers`  
    要发送的头部字典。

- `files`  
    用于 multipart 上传的 `{filename: fileobject}` 文件字典。

- `data`  
    附加到请求的正文。如果提供字典或元组列表 `[(key, value)]`，将进行表单编码。

- `json`  
    附加到请求正文的 json（如果未指定 `files` 或 `data`）。

- `params`  
    追加到 URL 的 URL 参数。如果提供字典或元组列表 `[(key, value)]`，将进行表单编码。

- `cookies`  
    要附加到此请求的 cookie 字典或 `CookieJar`。

用法：

```pycon
>>> import requests
>>> req = requests.Request('GET', 'https://httpbin.org/get')
>>> req.prepare()
<PreparedRequest [GET]>
```

#### prepare() → PreparedRequest

构造一个用于传输的 [`PreparedRequest`] 并返回它。

### class requests.Response —— 响应对象

https://requests.readthedocs.io/en/latest/api/#requests.Response

[`Response`] 对象包含服务器对 HTTP 请求的响应。

> 获取数据，并打印调试信息

#### 属性

- `property content: bytes`  
    响应的内容，以字节表示。
    > `b''` 原始字节

- `property text: str`  
    响应的内容，以 Unicode 表示。
    > 自动解码

    如果 `Response.encoding` 为 `None`，则将使用 `charset_normalizer` 或 `chardet` 猜测编码。

## Lower-Lower-Level Classes

https://requests.readthedocs.io/en/latest/api/#lower-lower-level-classes


### class requests.PreparedRequest

完全可变的 `PreparedRequest` 对象，包含将发送到服务器的确切字节。

> 调试时访问属性以打印请求各字段，方法目前未使用

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
    > `b''` 原始字节

## 请求会话

### class requests.Session

Requests 会话。

提供 `cookie` 持久化、连接池和配置。

#### `send()`

```py
send(request: PreparedRequest, **kwargs: Any) → Response
```

发送给定的 `PreparedRequest`。

- 返回类型  
    `requests.Response`

> `PreparedRequest` 本身不包含 `allow_redirects` 这类 flag，在 `requests.Session().send()` 中设置

```py
session = requests.Session()
res = session.send(pre_req, allow_redirects=False)
```