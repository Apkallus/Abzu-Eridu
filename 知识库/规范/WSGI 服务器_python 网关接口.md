https://wsgi.readthedocs.io/en/latest/what.html

## Definitions of keys and classes

https://wsgi.readthedocs.io/en/latest/definitions.html

### 标准 `environ` 键

- `REQUEST_METHOD`
  HTTP 请求方法，例如 `GET` 或 `POST`。这永远不能是空字符串，因此总是必需的。

- `SCRIPT_NAME`
  请求 URL 的“路径”中对应于应用程序对象的初始部分，以便应用程序知道其虚拟“位置”。如果应用程序对应于服务器的“根”，则这可以是空字符串。
    > 注意，空串将对应服务器根路径

- `PATH_INFO`
  请求 URL 的“路径”的其余部分，指定请求目标在应用程序内的虚拟“位置”。如果请求 URL 以应用程序根为目标且没有尾部斜杠，则这可以是空字符串。

- `QUERY_STRING`
  请求 URL 中跟在“?”之后的部分（如果有）。可以为空或不存在。

- `CONTENT_TYPE`
  HTTP 请求中任何 `Content-Type` 字段的内容。可以为空或不存在。

- `CONTENT_LENGTH`
  HTTP 请求中任何 `Content-Length` 字段的内容。可以为空或不存在。

- `SERVER_NAME`

- `SERVER_PORT`
  当与 `SCRIPT_NAME` 和 `PATH_INFO` 结合使用时，这些变量可用于补全 URL。但是请注意，如果存在 `HTTP_HOST`，在重建请求 URL 时应优先使用它而非 `SERVER_NAME`。有关更多详细信息，请参见下面的 URL 重建部分。`SERVER_NAME` 和 `SERVER_PORT` 永远不能是空字符串，因此总是必需的。

- `SERVER_PROTOCOL`
  客户端用于发送请求的协议版本。通常类似于“HTTP/1.0”或“HTTP/1.1”，应用程序可以使用它来确定如何处理任何 HTTP 请求头。（此变量可能应该称为 `REQUEST_PROTOCOL`，因为它表示请求中使用的协议，而不一定是服务器响应中将使用的协议。但是，为了与 CGI 兼容，我们必须保留现有名称。）

`HTTP_` 变量

> 对应于客户端提供的 HTTP 请求头的变量（即名称以 `HTTP_` 开头的变量）。这些变量的存在或不存在应与请求中相应 HTTP 头的存在或不存在相对应。