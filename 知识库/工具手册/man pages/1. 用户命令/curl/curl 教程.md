# curl 教程

https://curl.se/docs/tutorial.html

## 简单用法

从 Web 服务器获取主页：

```sh
curl https://www.example.com/
```

从 FTP 服务器获取 README 文件：

```sh
curl ftp://ftp.example.com/README
```

使用端口 8000 从服务器获取网页：

```sh
curl http://www.example.com:8000/
```

获取 FTP 站点的目录列表：

```sh
curl ftp://ftp.example.com/
```

从字典中获取所有匹配 curl 的词条：

```sh
curl dict://dict.example.com/m:curl
```

从字典中获取 curl 的定义：

```sh
curl dict://dict.example.com/d:curl
```

一次获取两个文档：

```sh
curl ftp://ftp.example.com/ https://www.example.com:8000/
```

从 FTPS 服务器获取文件：

```sh
curl ftps://files.are.example.com/secrets.txt
```

或者使用更合适的 FTPS 方式获取同一文件：

```sh
curl --ssl-reqd ftp://files.are.example.com/secrets.txt
```

使用 SFTP 从 SSH 服务器获取文件：

```sh
curl -u username sftp://example.com/etc/issue
```

使用 SCP 从 SSH 服务器获取文件，并使用私钥（未受密码保护）进行身份验证：

```sh
curl -u username: --key ~/.ssh/id_rsa scp://example.com/~/file.txt
```

使用 SCP 从 SSH 服务器获取文件，并使用私钥（受密码保护）进行身份验证：

```sh
curl -u username: --key ~/.ssh/id_rsa --pass private_key_password
  scp://example.com/~/file.txt
```

从 IPv6 Web 服务器获取主页：

```sh
curl "http://[2001:1890:1112:1::20]/"
```

## 下载到文件

获取网页并以指定名称存储到本地文件：

```sh
curl -o thatpage.html https://www.example.com/
```

获取网页并存储到本地文件，让本地文件使用远程文档的名称（如果 URL 中未指定文件名部分，则会失败）：

```sh
curl -O https://www.example.com/index.html
```

获取两个文件并以它们的远程名称存储：

```sh
curl -O www.haxx.se/index.html -O curl.se/download.html
```

## 使用密码

### FTP

要使用名称和密码进行 FTP 文件传输，请将它们包含在 URL 中，例如：

```sh
curl ftp://name:passwd@ftp.server.example:port/full/path/to/file
```

或者使用 `-u` 标志指定它们，例如：

```sh
curl -u name:passwd ftp://ftp.server.example:port/full/path/to/file
```

### FTPS

它类似 FTP，但你可能还希望指定并使用 SSL 特定选项，例如证书等。

注意，使用 `ftps://` 作为前缀是标准中描述的*隐式*方式，而推荐的*显式*方式是通过使用 `ftp://` 和 `--ssl-reqd` 选项来完成。

### SFTP / SCP

这类似 FTP，但你可以使用 `--key` 选项指定私钥来代替密码。注意，私钥本身可能受密码保护，该密码与远程系统的登录密码无关；此密码使用 `--pass` 选项指定。通常，curl 会自动从私钥文件中提取公钥，但在 curl 没有适当库支持的情况下，必须使用 `--pubkey` 选项指定匹配的公钥文件。

### HTTP

curl 也支持 HTTP(S) URL 中的用户和密码。你可以像这样下载文件：

```sh
curl https://name:passwd@http.server.example/full/path/to/file
```

或者像这样分别指定用户和密码：

```sh
curl -u name:passwd https://http.server.example/full/path/to/file
```

HTTP 提供许多不同的身份验证方法，curl 支持其中几种：Basic、Digest、NTLM 和 Negotiate（SPNEGO）。如果不告诉 curl 使用哪种方法，curl 默认使用 Basic。你也可以通过使用 `--anyauth`，让 curl 从服务器针对给定 URL 接受的方法中选择最安全的一种。

> **注意**！根据 URL 规范，HTTP URL 不能包含用户和密码，因此当通过代理使用 curl 时，这种风格不起作用，尽管 curl 在其他时候允许它。使用代理时，你*必须*使用 `-u` 风格来指定用户和密码。

### HTTPS

这最常与私有证书一起使用，如下所述。

## 代理

curl 支持 HTTP 和 SOCKS 代理服务器，并可选支持身份验证。它没有对 FTP 代理服务器的特殊支持，因为这类代理没有标准，但它仍然可以与许多 FTP 代理配合工作。你也可以使用 HTTP 和 SOCKS 代理在 FTP 服务器之间传输文件。

使用名为 `my-proxy`、端口为 888 的 HTTP 代理获取 FTP 文件：

```sh
curl -x my-proxy:888 ftp://ftp.example.com/README
```

使用上述同一代理，从需要用户名和密码的 HTTPS 服务器获取文件：

```sh
curl -u user:passwd -x my-proxy:888 https://www.example.com/
```

某些代理需要特殊身份验证。像上面一样使用 `-U` 指定：

```sh
curl -U user:passwd -x my-proxy:888 https://www.example.com/
```

可以指定不使用代理的主机和域的逗号分隔列表，如下所示：

```sh
curl --noproxy example.com -x my-proxy:888 https://www.example.com/
```

如果使用 `--proxy1.0` 而不是 `--proxy` 或 `-x` 指定代理，则 curl 在任何 `CONNECT` 尝试中使用 HTTP/1.0 而不是 HTTP/1.1。

curl 还通过 `--socks4` 和 `--socks5` 支持 SOCKS4 和 SOCKS5 代理。

另请参见 curl 支持的环境变量，它们提供进一步的代理控制。

大多数 FTP 代理服务器都设置为从客户端角度看像普通 FTP 服务器，并使用特殊命令来选择远程 FTP 服务器。curl 支持 `-u`、`-Q` 和 `--ftp-account` 选项，可用于通过许多 FTP 代理设置传输。例如，可以使用 Blue Coat FTP 代理将文件上传到远程 FTP 服务器，选项如下：

```sh
curl -u "username@ftp.server.example Proxy-Username:Remote-Pass"
  --ftp-account Proxy-Password --upload-file local-file
  ftp://my-ftp.proxy.example:21/remote/upload/path/
```

参见你的 FTP 代理手册以确定它期望何种形式来设置传输，并使用 curl 的 `-v` 选项查看 curl 实际发送的内容。

## 管道

获取密钥文件并将其安装为受信任密钥（在使用 `apt` 进行包管理的系统上）：

```sh
curl -L https://apt.example.org/llvm-snapshot.gpg.key | sudo tee
  /etc/apt/trusted.gpg.d/llvm-snapshot.asc >/dev/null
```

`|` 将输出管道到 stdin。`tee` 从 stdin 读取。

## 范围

HTTP 1.1 引入了字节范围。使用它，客户端可以请求仅获取指定文档的一个或多个子部分。curl 通过 `-r` 标志支持此功能。

获取文档的前 100 个字节：

```sh
curl -r 0-99 https://www.example.com/
```

获取文档的最后 500 个字节：

```sh
curl -r -500 https://www.example.com/
```

curl 也支持 FTP 文件的简单范围。这时你只能指定开始和停止位置。

使用 FTP 获取文档的前 100 个字节：

```sh
curl -r 0-99 ftp://www.example.com/README
```

## 上传

### FTP / FTPS / SFTP / SCP

将 stdin 上的所有数据上传到指定服务器：

```sh
curl -T - ftp://ftp.example.com/myfile
```

从指定文件上传数据，并使用用户名和密码登录：

```sh
curl -T uploadfile -u user:passwd ftp://ftp.example.com/myfile
```

将本地文件上传到远程站点，并在远程站点也使用本地文件名：

```sh
curl -T uploadfile -u user:passwd ftp://ftp.example.com/
```

上传本地文件并追加到远程文件：

```sh
curl -T localfile -a ftp://ftp.example.com/remotefile
```

curl 也支持通过代理进行 FTP 上传，但仅当代理配置为允许此类隧道时。如果允许，你可以类似这样运行 curl：

```sh
curl --proxytunnel -x proxy:port -T localfile ftp.example.com
```

### HTTP

将 stdin 上的所有数据上传到指定 HTTPS 站点：

```sh
curl -T - https://www.example.com/myfile
```

注意，必须已将 HTTP 服务器配置为接受 PUT，才能成功执行此操作。

有关进行 HTTP 数据上传的其他方式，请参见下面的 POST 部分。

## 详细输出 / 调试

如果 curl 在本不应失败的地方失败、服务器不让你进入、或者你无法理解响应：使用 `-v` 标志获取详细输出。curl 会输出大量信息以及它发送和接收的内容，以便用户看到所有客户端-服务器交互（但它不会向你显示实际数据）。

```sh
curl -v ftp://ftp.example.com/
```

要获取更多细节和关于 curl 所做操作的信息，请尝试使用 `--trace` 或 `--trace-ascii` 选项，并指定要记录到的文件名，如下所示：

```sh
curl --trace my-trace.txt www.haxx.se
```

## 详细信息

不同协议提供不同方式获取特定文件/文档的详细信息。要让 curl 显示单个文件的详细信息，应使用 `-I`/`--head` 选项。它会显示 HTTP 和 FTP 单个文件的所有可用信息。HTTP 信息要丰富得多。

对于 HTTP，你可以使用 `-i`/`--include` 在数据之前显示头部信息（与 `-I` 显示的内容相同）。curl 在从 FTP 和 HTTP 获取文件时理解 `-D`/`--dump-header` 选项，并会将头部存储到指定文件中。

将 HTTP 头部存储到单独文件（示例中为 `headers.txt`）：

```sh
  curl --dump-header headers.txt curl.se
```

注意，如果你希望 curl 以后使用服务器发送的 cookie，那么存储到单独文件中的头部可能有用。更多内容参见 cookie 部分。

## POST（HTTP）

使用 curl 提交数据很容易。这通过 `-d <data>` 选项完成。提交数据必须经过 URL 编码。

向一个简单的 `name` 和 `phone` 留言簿提交数据。

```sh
curl -d "name=Rafael%20Sagula&phone=3320780" https://www.example.com/guest.cgi
```

或者自动[对数据进行 URL 编码](https://everything.curl.dev/http/post/url-encode.html)。

```sh
curl --data-urlencode "name=Rafael Sagula&phone=3320780"
  https://www.example.com/guest.cgi
```

如何用 curl 提交表单，第 1 课：

找出你要填写的表单中的所有 `<input>` 标签。

如果是普通提交，你使用 `-d` 提交。`-d` 接受完整的提交字符串，格式为

```text
<variable1>=<data1>&<variable2>=<data2>&...
```

变量名是 `<input>` 标签中用 `"name="` 设置的名称，数据是你想为输入项填写的内容。数据*必须*经过正确的 URL 编码。这意味着你要用 `+` 替换空格，并用 `%XX` 替换特殊字母，其中 `XX` 是该字母 ASCII 码的十六进制表示。

示例：

（假设 `https://example.com` 有以下 HTML）

```html
<form action="post.cgi" method="post">
  <input name=user size=10>
  <input name=pass type=password size=10>
  <input name=id type=hidden value="blablabla">
  <input name=ding value="submit">
</form>
```

我们想输入用户 `foobar`，密码 `12345`。

要提交到这个表单，你会输入类似下面的 curl 命令行：

```sh
curl -d "user=foobar&pass=12345&id=blablabla&ding=submit"
  https://example.com/post.cgi
```

虽然 `-d` 使用 `application/x-www-form-urlencoded` MIME 类型（CGI 及类似程序普遍理解），curl 也支持能力更强的 `multipart/form-data` 类型。后一种类型支持文件上传等。

`-F` 接受类似 `-F "name=contents"` 的参数。如果你希望内容从文件读取，请使用 `@filename` 作为内容。指定文件时，你还可以通过在文件名后附加 `;type=<mime type>` 来指定文件内容类型。你也可以在一个字段中提交多个文件的内容。例如，字段名 `coolfiles` 用于发送三个文件，使用以下语法指定不同的内容类型：

```sh
curl -F "coolfiles=@fil1.gif;type=image/gif,fil2.txt,fil3.html"
  https://www.example.com/postit.cgi
```

如果未指定 content-type，curl 会尝试根据文件扩展名猜测（它只知道少数几种），或使用先前指定的类型（如果列表中指定了多个文件，则来自较早文件），否则使用默认类型 `application/octet-stream`。

用 `-F` 模拟填写表单。假设你在表单中填写三个字段。一个字段是要提交的文件名，一个字段是你的名字，一个字段是文件描述。我们想提交我们写好的名为 `cooltext.txt` 的文件。要让 curl 代替你喜欢的浏览器提交这些数据，你必须阅读表单页面的 HTML 源代码，找到输入字段的名称。在我们的示例中，输入字段名是 `file`、`yourname` 和 `filedescription`。

```sh
curl -F "file=@cooltext.txt" -F "yourname=Daniel"
  -F "filedescription=Cool text file with cool text inside"
  https://www.example.com/postit.cgi
```

要在一次提交中发送两个文件，可以通过两种方式做到：

在单个字段中用单个字段名发送多个文件：

```sh
curl -F "pictures=@dog.gif,cat.gif" $URL
```

用两个字段名发送两个字段

```sh
curl -F "docpicture=@dog.gif" -F "catpicture=@cat.gif" $URL
```

要按字面发送字段值，而不解释开头的 `@` 或 `<`，也不解释嵌入的 `;type=`，请使用 `--form-string` 而不是 `-F`。当值来自用户或其他不可预测来源时，建议这样做。在这些情况下，使用 `-F` 而不是 `--form-string` 可能允许用户欺骗 curl 上传文件。

## 引用来源

HTTP 请求可以选择包含关于哪个地址将其引用到实际页面的信息。curl 允许你在命令行上指定要使用的引用来源。这在欺骗或愚弄依赖该信息可用或包含特定数据的愚蠢服务器或 CGI 脚本时特别有用。

```sh
curl -e www.example.org https://www.example.com/
```

## 用户代理

HTTP 请求可以选择包含关于生成请求的浏览器的信息。curl 允许在命令行上指定它。这在欺骗或愚弄只接受某些浏览器的愚蠢服务器或 CGI 脚本时特别有用。

示例：

```sh
curl -A 'Mozilla/3.0 (Win95; I)' https://www.bank.example.com/
```

其他常见字符串：

- `Mozilla/3.0 (Win95; I)` - 用于 Windows 95 的 Netscape 版本 3
- `Mozilla/3.04 (Win95; U)` - 用于 Windows 95 的 Netscape 版本 3
- `Mozilla/2.02 (OS/2; U)` - 用于 OS/2 的 Netscape 版本 2
- `Mozilla/4.04 [en] (X11; U; AIX 4.2; Nav)` - 用于 AIX 的 Netscape
- `Mozilla/4.05 [en] (X11; U; Linux 2.0.32 i586)` - 用于 Linux 的 Netscape

注意，Internet Explorer 努力在各方面保持兼容：

- `Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)` - 用于 W95 的 MSIE

Mozilla 并不是唯一可能的 User-Agent 名称：

- `Konqueror/1.0` - KDE 文件管理器桌面客户端
- `Lynx/2.7.1 libwww-FM/2.14` - Lynx 命令行浏览器

## Cookie

Cookie 通常被 Web 服务器用于在客户端侧保存状态信息。服务器通过在头部发送类似 `Set-Cookie: <data>` 的响应行来设置 cookie，其中 data 部分通常包含一组 `NAME=VALUE` 对（用分号 `;` 分隔，如 `NAME1=VALUE1; NAME2=VALUE2;`）。服务器还可以指定 cookie 应用于什么路径（通过指定 `path=value`）、cookie 何时过期（`expire=DATE`）、用于什么域（`domain=NAME`）以及是否仅应在安全连接上使用（`secure`）。

如果你从服务器收到包含如下头部的页面：

```http
Set-Cookie: sessionid=boo123; path="/foo";
```

这意味着服务器希望当我们访问以 `/foo` 开头的路径中的任何内容时，传递第一个键值对。

示例，获取一个希望我的名字通过 cookie 传递的页面：

```sh
curl -b "name=Daniel" www.example.com
```

curl 还能够在后续会话中使用先前收到的 cookie。如果你从服务器获取 cookie 并以类似方式将它们存储到文件中：

```sh
curl --dump-header headers www.example.com
```

……然后你可以在第二次连接到该站点（或其他站点）时，像这样使用 `headers.txt` 文件中的 cookie：

```sh
curl -b headers.txt www.example.com
```

虽然将头部保存到文件是存储 cookie 的一种可行方式，但它容易出错，不是首选方式。相反，让 curl 使用众所周知的 Netscape cookie 格式保存传入的 cookie，如下所示：

```sh
curl -c cookies.txt www.example.com
```

注意，通过指定 `-b` 你启用了 cookie 引擎；使用 `-L` 可以让 curl 跟随 `location:`（它通常与 cookie 结合使用）。如果站点发送 cookie 和 location 字段，你可以使用一个不存在的文件来触发 cookie 感知，例如：

```sh
curl -L -b empty.txt www.example.com
```

读取 cookie 的文件必须使用普通 HTTP 头部格式或 Netscape cookie 文件格式。curl 根据文件内容确定它是哪种类型。在上面的命令中，curl 解析头部并存储从 [www.example.com](http://www.example.com) 收到的 cookie。curl 在跟随 location 时会将与请求匹配的已存储 cookie 发送给服务器。文件 `empty.txt` 可以是不存在的文件。

要从 Netscape cookie 文件读取和写入 cookie，可以将 `-b` 和 `-c` 都设置为使用同一文件：

```sh
curl -b cookies.txt -c cookies.txt www.example.com
```

## 进度条

进度条的存在是为了向用户显示确实有事情发生。输出中的不同字段含义如下：

```text
% Total    % Received % Xferd  Average Speed          Time             Curr.
                               Dload  Upload Total    Current  Left    Speed
0  151M    0 38608    0     0   9406      0  4:41:43  0:00:04  4:41:39  9287
```

从左到右：

- `%` - 整个传输完成的百分比
- `Total` - 整个预期传输的总大小
- `%` - 下载完成的百分比
- `Received` - 当前已下载的字节数
- `%` - 上传完成的百分比
- `Xferd` - 当前已上传的字节数
- `Average Speed Dload` - 下载的平均传输速度
- `Average Speed Upload` - 上传的平均传输速度
- `Time Total` - 完成操作的预期时间
- `Time Current` - 自调用以来经过的时间
- `Time Left` - 预计剩余完成时间
- `Curr.Speed` - 最近 5 秒的平均传输速度（当然，传输的前 5 秒基于更短时间。）

`-#` 选项显示完全不同的进度条，无需太多解释！

## 速度限制

curl 允许用户设置必须满足的传输速度条件，以让传输继续进行。通过使用 `-y` 和 `-Y` 开关，你可以让 curl 在传输速度低于指定最低限制达到指定时间时中止传输。

要让 curl 在速度低于每秒 3000 字节持续 1 分钟时中止下载，请运行：

```sh
curl -Y 3000 -y 60 www.far-away.example.com
```

这可以与总体时间限制结合使用，以便上述操作必须在 30 分钟内全部完成：

```sh
curl -m 1800 -Y 3000 -y 60 www.far-away.example.com
```

也可以强制 curl 不以高于给定速率传输数据，如果你使用有限带宽连接并且不希望传输占用全部带宽（有时称为*带宽限制*），这可能很有用。

让 curl 传输数据速度不超过每秒 10 KB：

```sh
curl --limit-rate 10K www.far-away.example.com
```

或

```sh
curl --limit-rate 10240 www.far-away.example.com
```

或者防止 curl 上传数据速度超过每秒 1 MB：

```sh
curl -T upload --limit-rate 1M ftp://uploads.example.com
```

使用 `--limit-rate` 选项时，传输速率按秒调节，这会导致总传输速度低于给定数字。有时当然会低很多，如果你的传输在某些时段停滞。

## 配置文件

curl 在启动时会自动尝试从用户主目录读取 `.curlrc` 文件（在 Microsoft Windows 系统上为 `_curlrc` 文件）。

配置文件可以由普通命令行开关组成，但你也可以省略破折号指定长选项，使其更易读。你可以用空格、`=` 或 `:` 分隔选项和参数。文件中可以使用注释。如果一行第一个字母是 `#` 符号，则该行其余部分被视为注释。

如果你希望参数包含空格，必须将整个参数括在双引号（`"`）中。在这些引号内，用 `\"` 指定引号。

注意：你必须将选项及其参数指定在同一行。

示例，在配置文件中设置默认超时和代理：

```text
# We want a 30 minute timeout:
-m 1800
#. .. and we use a proxy for all accesses:
proxy = proxy.our.domain.example.com:8080
```

行末的空白字符确实有意义，但每行第一个字符之前的所有空白都会被忽略。

通过将 `-q` 作为第一个命令行参数，防止 curl 读取默认文件，例如：

```sh
curl -q www.example.org
```

通过创建类似下面的配置文件，强制 curl 在没有 URL 调用时获取并显示本地帮助页面：

```text
# default URL to get
url = "https://help.with.curl.example.com/curlhelp.html"
```

你可以使用 `-K`/`--config` 标志指定要读取的另一个配置文件。如果将配置文件名设置为 `-`，它会从 stdin 读取配置，如果你想隐藏选项使其不出现在进程表等地方，这会很方便：

```sh
echo "user = user:passwd" | curl -K - https://that.secret.example.com
```

## 额外头部

在你自己的程序中使用 curl 时，你可能最终需要在获取网页时传递自己的自定义头部。你可以使用 `-H` 标志做到这一点。

示例，在获取页面时向服务器发送头部 `X-you-and-me: yes`：

```sh
curl -H "X-you-and-me: yes" love.example.com
```

如果你希望 curl 在头部中发送与通常不同的文本，这也很有用。你指定的 `-H` 头部会替换 curl 通常会发送的头部。如果你用一个空头部替换内部头部，就可以阻止发送该头部。要阻止使用 `Host:` 头部：

```sh
curl -H "Host:" server.example.com
```

## FTP 和路径名

请务必注意，使用 `ftp://` URL 获取文件时，给定路径相对于你进入的目录。要从 FTP 站点的主目录获取文件 `README`，请执行：

```sh
curl ftp://user:passwd@my.example.com/README
```

如果你想从同一站点的根目录获取 README 文件，需要指定绝对文件名：

```sh
curl ftp://user:passwd@my.example.com//README
```

（即在文件名前多一个斜杠。）

## SFTP 和 SCP 以及路径名

使用 `sftp:` 和 `scp:` URL 时，给定路径名是服务器上的绝对名称。要访问相对于远程用户主目录的文件，请在文件前加上 `/~/`，例如：

```sh
curl -u $USER sftp://home.example.com/~/.bashrc
```

## FTP 和防火墙

FTP 协议要求相关方之一在即将传输数据时打开第二个连接。有两种方式做到这一点。

curl 的默认方式是发出 `PASV` 命令，这会使服务器打开另一个端口并等待客户端执行另一次连接。如果客户端位于不允许传入连接的防火墙后面，这种方式很好。

```sh
curl ftp.example.com
```

如果服务器例如位于不允许 21 以外端口连接的防火墙后面（或者它不支持 `PASV` 命令），另一种方式是使用 `PORT` 命令，并指示服务器连接到给定 IP 号和端口（作为 `PORT` 命令的参数）上的客户端。

curl 的 `-P` 标志支持几个不同选项。你的机器可能有多个 IP 地址和/或网络接口，curl 允许你选择使用哪一个。也可以使用默认地址：

```sh
curl -P - ftp.example.com
```

使用 `PORT` 下载，但使用我们 `le0` 接口的 IP 地址（这在 Windows 上不起作用）：

```sh
curl -P le0 ftp.example.com
```

使用 `PORT` 下载，但使用 192.168.0.10 作为我们的 IP 地址：

```sh
curl -P 192.168.0.10 ftp.example.com
```

## 网络接口

使用指定接口端口从服务器获取网页：

```sh
curl --interface eth0:1 https://www.example.com/
```

或

```sh
curl --interface 192.168.1.10 https://www.example.com/
```

## HTTPS

安全 HTTP 需要安装并在构建 curl 时使用 TLS 库。如果已完成，curl 能够使用 HTTPS 协议检索和提交文档。

示例：

```sh
curl https://secure.example.com
```

curl 也能够使用客户端证书从要求有效证书的站点获取/提交文件。唯一缺点是证书需要为 PEM 格式。PEM 是一种用于存储证书的标准开放格式，但最常用的浏览器并不使用它。如果你希望 curl 使用你喜欢的浏览器所使用的证书，可能需要下载/编译一个转换器，将浏览器格式的证书转换为 PEM 格式。

示例，如何使用带个人密码的证书自动检索文档：

```sh
curl -E /path/to/cert.pem:password https://secure.example.com/
```

如果你忘记在命令行上指定密码，则在收到任何数据之前会提示你输入正确密码。

许多较旧的 HTTPS 服务器对较新版本 OpenSSL 等使用的特定 SSL 或 TLS 版本有问题，因此有时指定 curl 应使用哪个 TLS 版本很有用：

```sh
curl --tlv1.0 https://secure.example.com/
```

否则，curl 会尝试使用合理的默认 TLS 版本。

## 恢复文件传输

要从中断处继续文件传输，curl 支持 HTTP(S) 下载以及 FTP 上传和下载的恢复。

继续下载文档：

```sh
curl -C - -o file ftp://ftp.example.com/path/file
```

继续上传文档：

```sh
curl -C - -T file ftp://ftp.example.com/path/file
```

继续从 Web 服务器下载文档

```sh
curl -C - -o file https://www.example.com/
```

## 时间条件

HTTP 允许客户端为其请求的文档指定时间条件。它是 `If-Modified-Since` 或 `If-Unmodified-Since`。curl 允许你使用 `-z`/`--time-cond` 标志指定它们。

例如，你可以轻松地让下载仅在远程文件比本地副本新时执行。可以这样做：

```sh
curl -z local.html https://remote.example.com/remote.html
```

或者你可以仅在本地文件比远程文件新时下载文件。通过在日期字符串前加上 `-` 来做到这一点，例如：

```sh
curl -z -local.html https://remote.example.com/remote.html
```

你可以指定纯文本日期作为条件。告诉 curl 仅在文件自 2012 年 1 月 12 日以来更新过时下载它：

```sh
curl -z "Jan 12 2012" https://remote.example.com/remote.html
```

curl 接受多种日期格式。你总是可以通过在日期前加破折号（`-`）来反向进行日期检查。

## DICT

为了好玩，试试

```sh
curl dict://dict.org/m:curl
curl dict://dict.org/d:heisenbug:jargon
curl dict://dict.org/d:daniel:gcide
```

`m` 的别名是 `match` 和 `find`，`d` 的别名是 `define` 和 `lookup`。例如，

```sh
curl dict://dict.org/find:curl
```

打破 RFC 的 URL 描述（但不打破 DICT 协议）的命令是

```sh
curl dict://dict.org/show:db
curl dict://dict.org/show:strat
```

仍缺少身份验证支持

## LDAP

如果你已安装 OpenLDAP 库，curl 可以利用它并提供 `ldap://` 支持。在 Windows 上，curl 默认使用 Platform SDK 中的 WinLDAP。

curl 使用的默认协议版本是 LDAP 版本 3。版本 2 用作版本 3 连接失败时的回退机制。

LDAP 是一个复杂的东西，编写 LDAP 查询不是一件容易的事。请在其他地方熟悉确切的语法描述。一个这样的地方可能是：[RFC 2255, The LDAP URL Format](https://curl.se/rfc/rfc2255.txt)

给你一个示例，下面是如何从 LDAP 服务器获取电子邮件地址中包含某个子域的所有人员：

```sh
curl -B "ldap://ldap.example.com/o=frontec??sub?mail=*sth.example.com"
```

访问 LDAP 目录时也可以使用身份验证：

```sh
curl -u user:passwd "ldap://ldap.example.com/o=frontec??sub?mail=*"
curl "ldap://user:passwd@ldap.example.com/o=frontec??sub?mail=*"
```

默认情况下，如果提供了用户和密码，OpenLDAP/WinLDAP 使用基本身份验证。在 Windows 上，你可以通过在 curl 命令行中提供 `--basic`、`--ntlm` 或 `--digest` 选项之一来控制此行为

```sh
curl --ntlm "ldap://user:passwd@ldap.example.com/o=frontec??sub?mail=*"
```

在 Windows 上，如果未指定用户/密码，则使用当前登录凭据（SSPI/SPNEGO）进行自动协商。

## 环境变量

curl 读取并理解以下与代理相关的环境变量：

```text
http_proxy, HTTPS_PROXY, FTP_PROXY
```

它们应针对协议特定代理进行设置。通用代理应使用以下变量设置：

```text
ALL_PROXY
```

不应经过任何代理的主机名的逗号分隔列表设置在以下变量中（只有星号 `*` 匹配所有主机）：

```text
NO_PROXY
```

如果主机名匹配这些字符串之一，或主机位于这些字符串之一的域内，则与该节点的传输不通过代理进行。使用域时，需要以句点开头。用户可以通过将 `NO_PROXY` 设置为 `.example.com`，指定 [www.example.com](http://www.example.com) 和 foo.example.com 都不使用代理。通过包含完整名称，你可以排除特定主机名，因此要让 `www.example.com` 不使用代理但仍让 `foo.example.com` 使用代理，请将 `NO_PROXY` 设置为 `www.example.com`。

使用 `-x`/`--proxy` 标志会覆盖环境变量。

## Netrc

Unix 很久以前引入了 `.netrc` 概念。它让用户可以在文件中为常访问的 FTP 站点指定名称和密码，这样你每次访问这些站点时就不必输入它们。你意识到如果其他人拿到了你的密码，这是很大的安全风险，因此大多数 Unix 程序不会读取此文件，除非它仅你自己可读（不过 curl 不在乎）。

curl 支持 `.netrc` 文件（如果被告知使用，使用 `-n`/`--netrc` 和 `--netrc-optional` 选项）。这不限于 FTP，因此 curl 可以将其用于所有使用身份验证的协议。

一个简单的 `.netrc` 文件可能看起来像：

```text
machine curl.se login iamdaniel password mysecret
```

## 自定义输出

为了更好地让脚本程序员了解 curl 的进度，引入了 `-w`/`--write-out` 选项。使用它，你可以指定希望从先前传输中提取哪些信息。

要显示下载的字节数以及一些文本和结尾换行符：

```sh
curl -w 'We downloaded %{size_download} bytes\n' www.example.com
```

## Kerberos FTP 传输

curl 支持用于 FTP 传输的 kerberos4 和 kerberos5/GSSAPI。你需要安装 kerberos 包并在构建 curl 时使用它，才能使其可用。

首先，以正常方式获取 krb 票据，例如使用 `kinit`/`kauth` 工具。然后以类似方式使用 curl：

```sh
curl --krb private ftp://krb4site.example.com -u username:fakepwd
```

`-u` 开关上的密码没有用处，但空白密码会让 curl 询问密码，而你已经向 `kinit`/`kauth` 输入了真实密码。

## TELNET

curl 的 telnet 支持基本且易于使用。curl 将传递给它的 stdin 上的所有数据传递给远程服务器。使用类似以下命令连接到远程 telnet 服务器：

```sh
curl telnet://remote.example.com
```

在 stdin 上输入要传递给服务器的数据。结果发送到 stdout 或你使用 `-o` 指定的文件。

对于慢连接或类似情况，你可能希望使用 `-N`/`--no-buffer` 选项关闭缓冲输出。

通过使用 `-t` 选项向 telnet 协议协商传递选项。要告诉服务器我们使用 vt100 终端，可以尝试类似：

```sh
curl -tTTYPE=vt100 telnet://remote.example.com
```

`-t` 的其他有趣选项包括：

- `XDISPLOC=<X display>` 设置 X 显示位置。
- `NEW_ENV=<var,val>` 设置环境变量。

注意：telnet 协议没有规定任何使用指定用户名和密码登录的方式，因此 curl 无法自动做到这一点。要做到这一点，你需要跟踪何时收到登录提示，并相应地发送用户名和密码。

## 持久连接

在单个命令行上指定多个文件会使 curl 按指定顺序依次传输它们。

libcurl 尝试为传输使用持久连接，以便对同一主机的第二次传输可以使用已经发起并在先前传输中保持打开的同一连接。这大大减少了除第一次传输之外所有传输的连接时间，并更好地利用了网络。

注意，curl 不能为后续 curl 调用中的传输使用持久连接。如果多个 URL 使用同一主机，尽量在同一命令行上放置尽可能多的 URL，因为这会使传输更快。如果你使用 HTTP 代理进行文件传输，几乎所有传输都是持久的。

## 单个命令行进行多次传输

如上所述，你可以通过添加更多 URL 用一条命令行下载多个文件。如果你希望将它们保存到本地文件而不是打印到 stdout，则需要为你指定的每个 URL 添加一个保存选项。注意这也适用于 `-O` 选项（但不适用于 `--remote-name-all`）。

例如：获取两个文件，第一个使用 `-O`，第二个使用自定义文件名：

```sh
curl -O https://example.com/file.txt ftp://example.com/moo.exe -o moo.jpg
```

你也可以以类似方式上传多个文件：

```sh
curl -T local1 ftp://example.com/moo.exe -T local2 ftp://example.com/moo2.txt
```

## IPv6

当主机查找返回 IPv6 地址时，curl 使用 IPv6 连接服务器；如果连接失败，则回退到 IPv4。`--ipv4` 和 `--ipv6` 选项可以在两者都可用时指定使用哪个地址。IPv6 地址也可以使用以下语法直接在 URL 中指定：

```sh
https://[2001:1890:1112:1::20]/overview.html
```

使用这种风格时，必须给出 `-g` 选项，以阻止 curl 将方括号解释为特殊通配字符。链路本地和站点本地地址（包括作用域标识符，例如 `fe80::1234%1`）也可以使用，但作用域部分必须是数字或匹配 Linux 上现有的网络接口，并且百分号字符必须进行 URL 转义。上一个示例在 SFTP URL 中可能看起来像：

```sh
sftp://[fe80::1234%251]/
```

在 URL 之外提供的 IPv6 地址（例如提供给 `--proxy`、`--interface` 或 `--ftp-port` 选项）不应进行 URL 编码。

## 邮件列表

为方便起见，我们有几个开放的邮件列表，用于讨论 curl、其开发以及相关事项。请在 <https://curl.se/mail/> 获取所有信息。

请将 curl 问题、功能请求和故障报告发送到这些邮件列表之一，而不是发送给任何个人。

可用列表包括：

### `curl-users`

命令行工具的用户。如何使用它、什么不工作、新功能、相关工具、问题、新闻、安装、编译、运行、移植等。

### `curl-library`

使用或开发 libcurl 的开发者。缺陷、扩展、改进。

### `curl-announce`

低流量。仅接收新的公开版本公告。最坏情况下，每月大约一两封邮件，但通常每两个月只有一封邮件。

### `curl-and-php`

在 PHP 中使用 curl 函数。一切与 curl 相关的 PHP 角度。或者与 PHP 相关的 curl 角度。

### `curl-and-python`

使用 curl 的 Python 黑客，无论是否使用 Python 绑定 pycurl。