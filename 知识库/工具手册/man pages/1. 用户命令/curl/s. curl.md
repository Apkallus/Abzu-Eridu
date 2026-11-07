# curl

[官网文档](https://curl.se/docs/tooldocs.html)
- [手册](https://curl.se/docs/manpage.html)

[linux 手册](https://www.man7.org/linux/man-pages/man1/curl.1.html)

## 选项


### `-b, --cookie`

```
-b, --cookie <data|filename>
```

（HTTP）此选项有两个略有不同的 cookie 发送功能。

要么：将要发送到 HTTP 服务器的确切数据放入 `Cookie` 头中传递。这应该是先前从服务器在 `"Set-Cookie:"` 行中接收到的数据。数据格式应为 `"NAME1=VALUE1; NAME2=VALUE2"`。当给定一组特定 cookie 时，curl 会在所有传出请求中显式地用此内容填充其 cookie 头。如果由于身份验证、后续重定向或类似原因而执行多个请求，它们都会传递此 cookie 头。

或者：如果参数中未使用 `=` 符号，则将其视为文件名，从中读取先前存储的 cookie。此选项还会激活 cookie 引擎，使 curl 记录传入的 cookie；如果你将其与 [`--location`] 选项结合使用，或在同一次调用中执行多个 URL 传输，这可能很方便。

[`--cookie`] 可以在命令行中使用多次。

示例：

```sh
curl -b "" https://example.com
curl -b cookiefile https://example.com
curl -b name=Jane https://example.com
# 将 cookie 保存到 cookiefile 中，发送请求时携带，启用重定向。重定向的请求自动携带服务器响应设置的 cookie
curl -b cookiefile -c cookiefile -L https://example.com
```

另请参见 [`--cookie-jar`] 和 [`--junk-session-cookies`]。

### `-c, --cookie-jar`

```
-c, --cookie-jar <filename>
```

（HTTP）指定在操作完成后，你希望 curl 将所有 cookie 写入哪个文件。curl 在操作结束时将其内存中的 cookie 存储中的所有 cookie 写入给定文件。即使没有已知的 cookie，也会创建一个文件，以便从文件中移除任何先前存在的 cookie。该文件使用 Netscape cookie 文件格式。如果将文件名设置为单个减号 `-`，则 cookie 会写入标准输出。

如果多次提供 `[--cookie-jar]`，则使用最后设置的值。

示例：

```sh
curl -c store-here.txt https://example.com
curl -c store-here.txt -b read-these https://example.com
```

另请参见 `[--cookie]` 和 `[--junk-session-cookies]`。

### `--data-urlencode`

```
--data-urlencode <data>
```

(HTTP) 提交数据，类似于其他 `--data` 选项，不同之处在于此选项执行 URL 编码。

为了符合 CGI，`<data>` 部分应以 `name` 开头，后跟分隔符和内容说明。可以通过以下语法之一将 `<data>` 部分传递给 curl：

- `content`  
    对内容进行 URL 编码并传递。注意内容不要包含任何 `=` 或 `@` 符号，否则语法会匹配下面其他情况之一。

- `=content`  
    对内容进行 URL 编码并传递。前面的 `=` 符号不包含在数据中。

- `name=content`  
    对 `content` 部分进行 URL 编码并传递。注意 `name` 部分应已进行 URL 编码。
    > 注意，`name` 不被 URL 编码，且 `=` 后的所有内容均被 URL 编码。即，无法使用 `&` 设置多个参数，此时需多次使用 `--data-urlencode`

- `@filename`  
    从给定文件加载数据（包括任何换行符），对该数据进行 URL 编码，并在 POST 中传递。使用 `@-` 使 curl 从标准输入读取数据。

- `name@filename`  
    从给定文件加载数据（包括任何换行符），对该数据进行 URL 编码，并在 POST 中传递。`name` 部分会附加一个等号，结果为 `name=urlencoded-file-content`。注意 `name` 应已进行 URL 编码。

`--data-urlencode` 可以在命令行中多次使用。

示例：

```sh
# 发送多个 URL 编码的参数
curl --data-urlencode 'authcode=code_value' \
    --data-urlencode 'login_key=key_value' \
    --data-urlencode 'auth_token=token_value' \
    http://example.com

```

> 注意 curl 官网示例的 `--data-urlencode` 错误，无法在一个命令行参数值内包含多个请求体参数

另请参见 `--data` 和 `--data-raw`。


### `-L, --location`

(HTTP) 如果服务器报告请求的页面已移动到不同位置（由 `Location:` 标头和 3XX 响应码指示），此选项会让 curl 向新位置重新发起请求。默认不追踪重定向