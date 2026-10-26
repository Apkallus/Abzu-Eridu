# curl

[官网文档](https://curl.se/docs/tooldocs.html)
- [手册](https://curl.se/docs/manpage.html)

[linux 手册](https://www.man7.org/linux/man-pages/man1/curl.1.html)

```sh
curl [options / URLs]
```

参数
- `-I, --head`
	Fetch the headers only.
- `-i, --show-headers`  
	在输出中显示响应头。
- `-k, --insecure`
	(TLS SFTP SCP) 默认情况下，curl 建立的每个安全连接在传输之前都会验证其安全性。这个选项使 curl 跳过验证步骤，在不检查的情况下继续进行。
- `-L, --location`
	(HTTP) 如果服务器报告请求的页面已移动到不同位置（通过 Location: 标头和 3XX 响应代码指示），此选项会使 curl 重新向新位置发起请求。如果与 --show-headers 或 --head 一起使用，则会显示所有请求页面的标头。
- `-O，--remote-name` 
	下载的文件名使用原文件名
- `-S, --show-error` 
	失败时显示错误信息
- `-x, --proxy [protocol://]host[:port]` 
	Use the specified proxy.
- `-X, --request <method>` 
	修改请求方法
- `-H, --header <header/@file>`  
	在发送的信息中包含的额外头部

	```sh
	curl -H "Host: your.host" https://example.com
	```
- `-v, --verbose`  
	输出详细信息

- `--path-as-is` 
	向指定 URL 发出请求，而不删除点点斜杠序列(目录遍历)

## 参数

### `-b, --cookie`

```sh
-b, --cookie <data|filename>
```

（HTTP）此选项有两个略有不同的 cookie 发送功能。

要么：将要发送到 HTTP 服务器的确切数据放入 `Cookie` 头中传递。这应该是先前从服务器在 `"Set-Cookie:"` 行中接收到的数据。数据格式应为 `"NAME1=VALUE1; NAME2=VALUE2"`。当给定一组特定 cookie 时，curl 会在所有传出请求中显式地用此内容填充其 cookie 头。如果由于身份验证、后续重定向或类似原因而执行多个请求，它们都会传递此 cookie 头。

或者：如果参数中未使用 `=` 符号，则将其视为文件名，从中读取先前存储的 cookie。此选项还会激活 cookie 引擎，使 curl 记录传入的 cookie；如果你将其与 [`--location`] 选项结合使用，或在同一次调用中执行多个 URL 传输，这可能很方便。

如果文件名是单个减号（`"-"`），curl 从标准输入读取内容。如果文件名是空字符串（`""`）并且是唯一的 cookie 输入，curl 会在没有任何 cookie 的情况下激活 cookie 引擎。

要从中读取 cookie 的文件格式应为普通 HTTP 头（`Set-Cookie` 风格）或 Netscape/Mozilla cookie 文件格式。我们不鼓励使用 HTTP 头风格。

使用 [`--cookie`] 指定的文件仅用作输入。不会向该文件写入任何 cookie。要存储 cookie，请使用 [`--cookie-jar`] 选项。

如果你从普通 HTTP 头文件读取 cookie，请确保每个 `"Set-Cookie"` 行都指定了 `"Domain"` 属性。没有显式域，cookie 无法可靠地匹配到目标主机，并可能以意外方式应用。我们建议改用 Netscape 文件格式。

用户通常既想从文件读取 cookie，又想将更新后的 cookie 写回文件，因此在同一命令行中同时使用 [`--cookie`] 和 [`--cookie-jar`] 很常见。curl 会忽略使用 [`--cookie`] 指定的不存在或指向目录的文件名。

如果 curl 在构建时支持 PSL（`Public Suffix List`，公共后缀列表），它会检测并丢弃为那些不应允许拥有 cookie 的后缀域指定的 cookie。如果 curl 在构建时*不*支持 PSL，它就无法阻止超级 cookie。

[`--cookie`] 可以在命令行中使用多次。

示例：

```sh
curl -b "" https://example.com
curl -b cookiefile https://example.com
curl -b cookiefile -c cookiefile https://example.com
curl -b name=Jane https://example.com
```

另请参见 [`--cookie-jar`] 和 [`--junk-session-cookies`]。

### `-c, --cookie-jar`

```sh
-c, --cookie-jar <filename>
```

（HTTP）指定在操作完成后，你希望 curl 将所有 cookie 写入哪个文件。curl 在操作结束时将其内存中的 cookie 存储中的所有 cookie 写入给定文件。即使没有已知的 cookie，也会创建一个文件，以便从文件中移除任何先前存在的 cookie。该文件使用 Netscape cookie 文件格式。如果将文件名设置为单个减号 `-`，则 cookie 会写入标准输出。

使用 `[--cookie-jar]` 指定的文件仅用于输出。不会从该文件读取任何 cookie。要读取 cookie，请使用 `[--cookie]` 选项。两个选项可以指定同一个文件。

此命令行选项会激活 cookie 引擎，使 curl 记录并使用 cookie。`[--cookie]` 选项也会激活它。

如果无法创建或写入 cookie jar，整个 curl 操作不会失败，甚至不会清楚地报告错误。使用 `[--verbose]` 会显示警告，但这是你关于这种可能致命的情况所能获得的唯一可见反馈。

你可能希望限制 umask，以防止同一系统上的其他用户访问创建的文件。

如果多次提供 `[--cookie-jar]`，则使用最后设置的值。

示例：

```sh
curl -c store-here.txt https://example.com
curl -c store-here.txt -b read-these https://example.com
```

另请参见 `[--cookie]` 和 `[--junk-session-cookies]`。

### `-d, --data`

```sh
-d, --data <data>
```

（HTTP MQTT）将指定数据发送到服务器。

对于 HTTP(S)，这通过 POST 方法完成，方式与用户在浏览器中填写 HTML 表单并按下提交按钮时相同。此选项使 curl 使用内容类型 `application/x-www-form-urlencoded` 将数据传递给服务器。

对于 MQTT，数据作为 PUBLISH 发送。

`--data-raw` 几乎相同，但不会对 `@` 字符进行特殊解释。要提交纯二进制数据，应改用 `--data-binary` 选项。要对表单字段的值进行 URL 编码，可以使用 `--data-urlencode`。

如果这些选项中的任何一个在同一命令行上使用多次，指定的数据片段会用 `&` 符号分隔合并。因此，使用 `-d name=daniel -d skill=lousy` 会生成类似 `name=daniel&skill=lousy` 的提交块。

如果数据以字母 `@` 开头，其余部分应是用于读取数据的文件名；如果希望 curl 从标准输入读取数据，则使用 `-`。因此，从名为 `foobar` 的文件提交数据可通过 `--data @foobar` 完成。当 `--data` 被告知以这种方式从文件读取时，回车符、换行符和空字节会被剥离。如果你不希望 `@` 字符具有特殊解释，请改用 `--data-raw`。

此选项的数据会完全按照命令行上提供的内容传递给服务器。curl 不会转换、更改或改进它。用户有责任以正确形式提供数据。

`--data` 可以在命令行中使用多次。

示例：

```sh
curl -d "name=curl" https://example.com
curl -d "name=curl" -d "tool=cmdline" https://example.com
curl -d @filename https://example.com
```

此选项与 `--form`、`--head` 和 `--upload-file` 互斥。另请参见 `--data-binary`、`--data-urlencode`、`--data-raw` 和 `--form`。

### `-s, --silent`

静默或安静模式。不显示进度条、提示消息、警告消息或错误消息。使 curl 保持沉默。它仍然输出你请求的数据，甚至可能输出到终端/标准输出，除非你重定向它。

将此选项与 `[--show-error]` 一起使用，可禁用进度条但仍显示错误消息。

多次提供 `--silent` 没有额外效果。使用 `--no-silent` 可再次禁用它。

示例：

```sh
curl -s https://example.com
```

另请参见 `[--verbose]`、`[--stderr]` 和 `[--no-progress-meter]`。

### `-o, --output`

将输出写入给定文件而不是标准输出。如果你在 URL 中使用通配来获取多个文档，应该给 URL 加上引号，并且可以在文件名中使用 `#` 后跟一个数字。该变量会被替换为当前通配文本。例如：

```sh
curl "http://{one,two}.example.com" -o "file_#1.txt"
```

或者使用多个变量，例如：

```sh
curl "http://{site,host}.host[1-5].example" -o "#1_#2"
```

你可以根据 URL 数量多次使用此选项。例如，如果在同一命令行上指定两个 URL，可以这样使用：

```sh
curl -o aa example.com -o bb example.net
```

并且 `-o` 选项与 URL 的顺序无关，只要第一个 `-o` 对应第一个 URL，依此类推，因此上面的命令行也可以写成：

```sh
curl example.com example.net -o aa -o bb
```

另请参见 `[--create-dirs]` 选项，以动态创建本地目录。将输出指定为 `-`（单个破折号）会将输出传递到标准输出。

要抑制响应正文，可以将输出重定向到 `/dev/null`：

```sh
curl example.com -o /dev/null
```

或在 Windows 上：

```sh
curl example.com -o nul
```

或者，更高效且可移植的方式是使用：

```sh
curl example.com --out-null
```

将文件名指定为单个减号可强制输出到标准输出，以覆盖 curl 内部对终端二进制输出的阻止：

```sh
curl https://example.com/jpeg -o -
```

注意，二进制输出可能是由响应被压缩引起的，这种情况下你可能想使用 `[--compressed]` 选项。

自 curl 8.21.0 起，可以给独立的通配部分命名，并通过名称引用它们。区分大小写的字母数字名称在开括号字符之后用尖括号括起来设置。示例：

```sh
curl "https://fun.example/{<num>one,two}.jpg" -o "save-#<num>"
 
curl "ftp://ftp.example/file[<range>1-100].txt" \
  -o "save-#<range>.txt"
```

引用未设置的命名通配会导致错误。

自 curl 8.21.0 起，当上传文件名使用通配时，你可以使用其部分内容：设置一个通配名称，并像引用命名 URL 通配一样引用它。例如，如果你将三个文件上传到单个固定 HTTP URL，并希望将对应的响应保存到不同文件中：

```sh
curl -T 'file{<num>1,2,3}' \
  https://upload.example/ -o 'response-#<num>'
```

`[--output]` 与单个 URL 关联。当你在命令行中使用多个 URL 时，为每个 URL 使用一次。

示例：

```sh
curl -o file https://example.com
curl "http://{one,two}.example.com" -o "file_#1.txt"
curl "http://{site,host}.host[1-5].example" -o "#1_#2"
curl -o file https://example.com -o file2 https://example.net
```

另请参见 `[--out-null]`、`[--remote-name]`、`[--remote-name-all]`、`[--remote-header-name]` 和 `[--compressed]`。