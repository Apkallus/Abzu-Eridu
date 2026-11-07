https://requests.readthedocs.io/en/latest/api/#lower-level-classes

## 底层类

### class requests.Request()

```py
class requests.Request(method: str | None = None, url: _t.UriType | None = None, headers: _t.HeadersType = None, files: _t.FilesType = None, data: _t.DataType = None, params: _t.ParamsType = None, auth: _t.AuthType = None, cookies: RequestsCookieJar | CookieJar | dict[str, str] | None = None, hooks: _t.HooksInputType | None = None, json: _t.JsonType = None)
```

用户创建的 [`Request`] 对象。

用于准备 [`PreparedRequest`]，并将其发送到服务器。

**参数：**

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

- `auth`  
    认证处理器或 `(user, pass)` 元组。

- `cookies`  
    要附加到此请求的 cookie 字典或 `CookieJar`。

- `hooks`  
    回调钩子字典，供内部使用。

用法：

```pycon
>>> import requests
>>> req = requests.Request('GET', 'https://httpbin.org/get')
>>> req.prepare()
<PreparedRequest [GET]>
```

#### deregister_hook() → bool

```py
deregister_hook(event: str, hook: Callable[[Response], Any]) → bool
```

注销先前注册的钩子。如果钩子存在则返回 `True`，否则返回 `False`。

#### prepare() → PreparedRequest

构造一个用于传输的 [`PreparedRequest`] 并返回它。

#### register_hook() → None

```py
register_hook(event: str, hook: Iterable[Callable[[Response], Any]] | Callable[[Response], Any]) → None
```

正确注册一个钩子。

### class requests.Response

[`Response`] 对象包含服务器对 HTTP 请求的响应。

- `property apparent_encoding: str | None`  
    表观编码，由 `charset_normalizer` 或 `chardet` 库提供。

- 
    ```py
    close() → None
    ```

    将连接释放回连接池。调用此方法后，不得再次访问底层的 `raw` 对象。

    *注意：通常不需要显式调用。*

- `property content: bytes`  
    响应的内容，以字节表示。

- `cookies: RequestsCookieJar`  
    服务器返回的 Cookie 的 `CookieJar`。

- `elapsed: datetime.timedelta`  
    从发送请求到响应到达之间经过的时间（以 `timedelta` 表示）。此属性专门测量从发送请求的第一个字节到完成解析响应头所花费的时间。因此，它不受消费响应内容或 `stream` 关键字参数值的影响。

- `encoding: str | None`  
    访问 `r.text` 时用于解码的编码。

- `headers: CaseInsensitiveDict[str]`  
    响应头的忽略大小写字典。例如，`headers['content-encoding']` 将返回 `'Content-Encoding'` 响应头的值。

- `history: list[Response]`  
    来自请求历史的 [`Response`] 对象列表。任何重定向响应都会出现在这里。该列表按从最早到最近请求排序。

- `property is_redirect: bool`  
    如果此 Response 是格式良好的 HTTP 重定向，并且可以由 [`Session.resolve_redirects`] 自动处理，则为 `True`。

- 
    ```py
    iter_content(chunk_size: int | None = 1, decode_unicode: Literal[False] = False) → Iterator[bytes]
    iter_content(chunk_size: int | None = 1, *, decode_unicode: Literal[True]) → Iterator[str | bytes]
    ```

    遍历响应数据。当在请求上设置 `stream=True` 时，这可避免将大型响应的内容一次性读入内存。`chunk_size` 是应读入内存的字节数。由于可能发生解码，它不一定是返回的每个项的长度。

    `chunk_size` 必须是 `int` 或 `None`。值 `None` 的行为取决于 `stream` 的值。`stream=True` 将按接收到的块大小读取数据。如果 `stream=False`，数据将作为单个块返回。

    如果 `decode_unicode` 为 `True`，将使用响应中的编码信息解码内容。如果没有可用的编码信息，将返回字节。可以通过在响应上手动设置 `encoding` 来绕过这一点。

- 
    ```py
    iter_lines(chunk_size: int = ITER_CHUNK_SIZE, decode_unicode: Literal[False] = False, delimiter: bytes | None = None) → Iterator[bytes]
    iter_lines(chunk_size: int = ITER_CHUNK_SIZE, *, decode_unicode: Literal[True], delimiter: str | bytes | None = None) → Iterator[str | bytes]
    ```

    逐行遍历响应数据。当在请求上设置 `stream=True` 时，这可避免将大型响应的内容一次性读入内存。

    `decode_unicode` 参数的工作方式与 `iter_content` 中相同，并具有相同的注意事项。

    > **注意**
    >
    > 此方法不是可重入安全的。

- 
    ```py
    json(**kwargs: Any) → Any
    ```

    将 JSON 响应体（如果有）解码为 Python 对象。

    根据响应中的内容，这可能返回字典、列表等。

    **参数：**

    - `**kwargs`  
        `json.loads` 接受的可选参数。

    **异常：**

    - [`requests.exceptions.JSONDecodeError`]  
        如果响应体不包含有效的 json。

- `property links: dict[str, dict[str, str]]`  
    返回响应中解析出的头部链接（如果有）。

- `property next: PreparedRequest | None`  
    如果重定向链中存在下一个请求，则返回其 `PreparedRequest`。

- `property ok: bool`  
    如果 [`status_code`] 小于 400，则返回 `True`，否则返回 `False`。

    此属性检查响应的状态码是否在 400 到 600 之间，以判断是否存在客户端错误或服务器错误。如果状态码在 200 到 400 之间，则返回 `True`。这 **不是** 检查响应码是否为 `200 OK`。

- 
    ```py
    raise_for_status() → None
    ```

    如果发生错误，则引发 [`HTTPError`]。

- `raw: Any`  
    响应的类文件对象表示（用于高级用法）。使用 `raw` 要求在请求上设置 `stream=True`。此要求不适用于 Requests 内部使用。

- `reason: str`  
    响应 HTTP 状态的原因短语，例如 “Not Found” 或 “OK”。

- `request: PreparedRequest`  
    此响应所对应的 [`PreparedRequest`] 对象。

- `status_code: int`  
    响应 HTTP 状态的整数代码，例如 404 或 200。

- `property text: str`  
    响应的内容，以 Unicode 表示。

    如果 `Response.encoding` 为 `None`，则将使用 `charset_normalizer` 或 `chardet` 猜测编码。

    响应内容的编码仅根据 HTTP 头确定，严格遵循 RFC 2616。如果你可以利用非 HTTP 知识来更好地猜测编码，应在访问此属性之前适当设置 `r.encoding`。

- `url: str`  
    Response 的最终 URL 位置。