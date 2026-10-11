[速查表](https://httpd.apache.org/docs/2.4/en/mod/quickreference.html)

## Configuration Files —— 配置文件

https://httpd.apache.org/docs/2.4/configuring.html

本文件描述用于配置 Apache HTTP 服务器的文件。

### 主配置文件

Apache HTTP 服务器通过在纯文本配置文件中放置[指令](mod/directives.html)来进行配置。主配置文件通常称为 `httpd.conf`。此文件的位置在编译时设置，但可以通过 `-f` 命令行标志覆盖。此外，可以使用 [`Include`](mod/core.html#include) 指令添加其他配置文件，并且可以使用通配符来包含许多配置文件。任何指令都可以放置在这些配置文件中的任何一个中。对主配置文件的更改仅在 httpd 启动或重新启动时被识别。

服务器还会读取一个包含 mime 文档类型的文件；文件名由 [`TypesConfig`](mod/mod_mime.html#typesconfig) 指令设置，默认为 `mime.types`。

### 配置文件的语法

httpd 配置文件每行包含一条指令。反斜杠 `\` 可用作行末的最后一个字符，表示该指令延续到下一行。要被解释为这种续行，反斜杠与行末之间不能有其他字符或空白。

以井号字符 `#` 开头的行被视为注释，并被忽略。注释**不能**与配置指令包含在同一行，包括上文所述的已续行的行首。被注释的行也可以续行，这意味着下一个物理行也会被解释为注释，因为逻辑行以井号字符开头。

指令之前的空白会被忽略，因此为了清晰而对指令进行缩进。空行也会被忽略。指令的参数由空白分隔。如果参数包含空格，则必须将该参数用引号括起来。

#### 引号和转义

双引号（`"`）或单引号（`'`）都可用于括住包含空格的参数。引号本身不是参数的一部分。

在带引号的字符串内，只识别两个转义序列：`\\` 产生一个字面反斜杠，`\"`（如果字符串是单引号的，则为 `\'`）产生一个字面引号字符而不结束字符串。所有其他反斜杠序列都会原样传递——例如，`\n` 是两个字面字符 `\n`，而不是换行符。

在引号外，反斜杠没有特殊含义，被视为字面字符。唯一的例外是如上所述位于行末的续行反斜杠。

请注意，相邻的带引号字符串之间没有空白时**不会**被连接——它们会被解析为单独的参数。例如：

```
# 这是两个参数，不是一个：
Header set X-Foo "bar""baz"
```

一些指令接受包含具有自己语法的子表达式的参数，例如 [`RewriteRule`](mod/mod_rewrite.html#rewriterule) 标志或 [ap_expr](expr.html) 表达式。在这些情况下，配置文件解析器首先移除包围的引号并如上所述处理反斜杠转义，然后指令自己的解析器处理结果。如有疑问，对包含反斜杠的参数使用单引号可以避免转义序列的意外双重处理。

配置文件中的指令不区分大小写，但指令的参数通常区分大小写。

使用 [`Define`](mod/core.html#define) 定义的变量或 shell 环境变量的值可以在配置文件行中使用语法 `${VAR}`。如果 "VAR" 是有效变量的名称，则该变量的值会被替换到配置文件行中的该位置，处理继续，就像该文本直接出现在配置文件中一样。使用 [`Define`](mod/core.html#define) 定义的变量优先于 shell 环境变量。如果未找到 "VAR" 变量，则字符 `${VAR}` 保持不变，并记录警告。变量名不能包含冒号 ":" 字符，以避免与 [`RewriteMap`](mod/mod_rewrite.html#rewritemap) 的语法冲突。

只有在服务器启动之前定义的 shell 环境变量才能用于扩展。在配置文件本身中定义的环境变量（例如使用 [`SetEnv`](mod/mod_env.html#setenv)）生效太晚，无法用于配置文件中的扩展。

正常配置文件中一行的最大长度（在变量替换和连接任何续行之后）约为 16 MiB。在 [.htaccess 文件](#htaccess)中，最大长度为 8190 个字符。

使用 `apachectl configtest` 或 `-t` 命令行选项来检查配置文件的语法错误，而无需启动服务器。

使用 [`mod_info`](mod/mod_info.html) 的 `-DDUMP_CONFIG` 来转储配置，其中所有包含的文件和环境变量都已解析，所有注释以及不匹配的 [`<IfDefine>`](mod/core.html#ifdefine) 和 [`<IfModule>`](mod/core.html#ifmodule) 部分都已移除。但是，输出不会反映重复指令可能发生的合并或覆盖。

### 模块

httpd 是一个模块化服务器。这意味着核心服务器中只包含最基本的功能。扩展功能通过可加载到 httpd 中的[模块](mod/)提供。默认情况下，在编译时会在服务器中包含一组[基础](mod/module-dict.html#Status)模块。如果服务器编译为使用[动态加载](dso.html)模块，则模块可以单独编译，并随时使用 [`LoadModule`](mod/mod_so.html#loadmodule) 指令添加。否则，必须重新编译 httpd 才能添加或移除模块。配置指令可以通过将它们括在 [`<IfModule>`](mod/core.html#ifmodule) 块中来根据特定模块的存在情况有条件地包含。但是，[`<IfModule>`](mod/core.html#ifmodule) 块不是必需的，在某些情况下可能会掩盖你缺少重要模块的事实。

要查看当前编译到服务器中的模块，使用 `-l` 命令行选项。你还可以使用 `-M` 命令行选项查看动态加载了哪些模块。

### 指令的作用域

放置在主配置文件中的指令应用于整个服务器。如果你希望仅更改服务器某一部分的配置，可以通过将指令放置在 [`<Directory>`]、[`<DirectoryMatch>`]、[`<Files>`]、[`<FilesMatch>`]、[`<Location>`] 和 [`<LocationMatch>`] 部分中来限定其作用域。这些部分将其包含的指令的应用限制到特定的文件系统位置或 URL。它们还可以嵌套，从而实现非常细粒度的配置。

httpd 能够同时服务许多不同的网站。这称为[虚拟主机](vhosts/)。指令也可以通过将它们放置在 [`<VirtualHost>`](mod/core.html#virtualhost) 部分中来限定作用域，以便它们仅适用于对特定网站的请求。

尽管大多数指令可以放置在这些部分中的任何一个中，但有些指令在某些上下文中没有意义。例如，控制进程创建的指令只能放置在主服务器上下文中。要了解哪些指令可以放置在哪些部分中，请检查该指令的[上下文](mod/directive-dict.html#Context)。有关更多信息，我们提供了关于[目录、位置和文件部分如何工作](sections.html)的详细信息。

### .htaccess 文件

httpd 允许通过放置在 web 树内的特殊文件进行分散式配置管理。这些特殊文件通常称为 `.htaccess`，但可以在 [`AccessFileName`](mod/core.html#accessfilename) 指令中指定任何名称。放置在 `.htaccess` 文件中的指令应用于你放置该文件的目录以及所有子目录。`.htaccess` 文件遵循与主配置文件相同的语法。由于 `.htaccess` 文件在每次请求时都会被读取，因此在这些文件中所做的更改会立即生效。

要了解哪些指令可以放置在 `.htaccess` 文件中，请检查该指令的[上下文](mod/directive-dict.html#Context)。服务器管理员通过在主配置文件中配置 [`AllowOverride`](mod/core.html#allowoverride) 指令进一步控制哪些指令可以放置在 `.htaccess` 文件中。

有关 `.htaccess` 文件的更多信息，请参阅 [.htaccess 教程](howto/htaccess.html)。

## How-To / Tutorials —— 教程

### .htaccess files —— 目录级配置文件

docs
- [apache](https://httpd.apache.org/docs/current/howto/htaccess.html)

- [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Apache_Configuration_htaccess)

## Modules

### Directive Quick Reference —— 速查表

https://httpd.apache.org/docs/2.4/en/mod/quickreference.html

### Apache Core Features

https://httpd.apache.org/docs/2.4/en/mod/core.html

#### HttpProtocolOptions Directive 

https://httpd.apache.org/docs/2.4/en/mod/core.html#httpprotocoloptions

##### Strict|Unsafe —— CTF 配置

在引入此指令之前，Apache HTTP Server 请求消息解析器容忍多种不符合协议的输入形式。[RFC 7230](https://www.rfc-editor.org/rfc/rfc7230#section-9.4)（请求拆分）和 [RFC 7230](https://www.rfc-editor.org/rfc/rfc7230#section-9.5)（响应走私）仅指出了接受非合规请求消息的两种潜在风险，而 [RFC 7230](https://www.rfc-editor.org/rfc/rfc7230#section-3.5) "Message Parsing Robustness" 则指出了接受模糊空白和请求消息格式的风险。自引入此指令起，规范的所有语法规则都在默认的 `Strict` 操作模式下强制执行，并且第 3.5 节建议的严格空白被强制执行且无法放宽。

> **Unsafe 的安全风险**
>
> 强烈警告用户不要切换 `Unsafe` 操作模式，尤其是在面向外部、可公开访问的服务器部署上。如果内部网上运行的故障监控或其他自定义服务消费者需要某个接口，用户应仅在配置为服务其内部专用网络的特定虚拟主机上切换 Unsafe 选项。

在严格模式下导致 400 响应的示例：

```http
# Missing CRLF
GET / HTTP/1.0\n\n 
```

#### `<VirtualHost>` 指令

https://httpd.apache.org/docs/2.4/en/mod/core.html#virtualhost

- 描述：包含仅适用于特定主机名或 IP 地址的指令
- 语法：`<VirtualHost addr[:port] [addr[:port]] ...> ... </VirtualHost>`
- 上下文：server config
- 状态：Core
- 模块：core

`<VirtualHost>` 和 `</VirtualHost>` 用于括起一组仅适用于特定虚拟主机的指令。任何允许在虚拟主机上下文中使用的指令都可以使用。当服务器收到对特定虚拟主机上文档的请求时，它会使用 `<VirtualHost>` 部分中包含的配置指令。`addr` 可以是以下任意一种，可选地后跟冒号和端口号（或 `*`）：

- 虚拟主机的 IP 地址；
- 虚拟主机 IP 地址的完全限定域名（不推荐）；
- 字符 `*`，作为通配符，匹配任何 IP 地址。
- 字符串 `_default_`，它是 `*` 的别名

```conf
<VirtualHost 10.1.2.3:80>
  ServerAdmin webmaster@host.example.com
  DocumentRoot "/www/docs/host.example.com"
  ServerName host.example.com
  ErrorLog "logs/host.example.com-error_log"
  TransferLog "logs/host.example.com-access_log"
</VirtualHost>
```

IPv6 地址必须在方括号中指定，因为否则无法确定可选端口号。IPv6 示例如下：

```conf
<VirtualHost [2001:db8::a00:20ff:fea7:ccea]:80>
  ...
</VirtualHost>
```

每个虚拟主机必须对应不同的 IP 地址、不同的端口号或服务器的不同主机名，在前一种情况下，服务器机器必须配置为接受多个地址的 IP 数据包。（如果机器没有多个网络接口，那么可以使用 `ifconfig alias` 命令实现——如果你的操作系统支持的话）。

> **注意**
>
> 使用 `<VirtualHost>` **不会**影响 Apache httpd 监听的地址。你可能需要使用 [`Listen`](../mod/mpm_common.html#listen) 确保 Apache httpd 监听正确的地址。

应在每个 `<VirtualHost>` 块内指定 [`ServerName`](#servername)。如果缺失，将继承“主”服务器配置中的 [`ServerName`](#servername)。

当收到请求时，服务器首先仅基于本地 IP 地址和端口组合将其映射到最匹配的 `<VirtualHost>`。非通配符具有更高的优先级。如果完全没有基于 IP 和端口的匹配，则使用“主”服务器配置。

如果多个虚拟主机包含最佳匹配的 IP 地址和端口，服务器会根据请求的主机名从这些虚拟主机中选择最佳匹配。如果未找到匹配的基于名称的虚拟主机，则使用匹配该 IP 地址的第一个列出的虚拟主机。因此，对于给定 IP 地址和端口组合，第一个列出的虚拟主机是该 IP 和端口组合的默认虚拟主机。

> **安全**
>
> 有关如果存储日志文件的目录可被除启动服务器的用户以外的任何人写入，你的安全性可能受到损害的详细信息，请参阅[安全提示](../misc/security_tips.html)文档。

##### 参阅

- [Apache HTTP Server 虚拟主机文档](../vhosts/)
- [关于 DNS 和 Apache HTTP Server 的问题](../dns-caveats.html)
- [设置 Apache HTTP Server 使用的地址和端口](../bind.html)
- [`<Directory>`、`<Location>` 和 `<Files>` 部分如何工作](../sections.html)，以解释收到请求时这些不同部分如何组合

### AliasMatch 指令 —— 使用正则表达式将 URL 映射到文件系统

https://httpd.apache.org/docs/2.4/en/mod/mod_alias.html#aliasmatch

- 描述：使用正则表达式将 URL 映射到文件系统位置
- 语法：`AliasMatch regex file-path|directory-path`
- 上下文：server config, virtual host
- 状态：Base
- 模块：mod_alias

此指令等同于 [`Alias`](#alias)，但使用[正则表达式](https://httpd.apache.org/docs/current/glossary.html#regex)而非简单的前缀匹配。所提供的正则表达式会与 URL 路径进行匹配，如果匹配成功，服务器会将任何括号内的匹配内容替换到给定字符串中，并将其用作文件名。例如，要激活 `/icons` 目录，可以使用：

```apache
AliasMatch "^/icons(/|$)(.*)" "/usr/local/apache/icons$1$2"
```

可以使用[正则表达式](https://httpd.apache.org/docs/current/glossary.html#regex)的全部功能。例如，可以构造一个对 URL 路径进行不区分大小写匹配的别名：

```apache
AliasMatch "(?i)^/image(.*)" "/ftp/pub/image$1"
```

[`Alias`](#alias) 和 `AliasMatch` 之间的一个细微区别是，[`Alias`](#alias) 会自动将 URI 中匹配部分之后的任何额外部分复制到右侧文件路径的末尾，而 `AliasMatch` 不会。这意味着在几乎所有情况下，你都会希望正则表达式从头到尾匹配整个请求 URI，并在右侧使用替换。

换句话说，仅仅将 [`Alias`](#alias) 改为 `AliasMatch` 不会产生相同的效果。至少，你需要在正则表达式的开头添加 `^`，在末尾添加 `(.*)$`，并在替换的末尾添加 `$1`。

例如，假设你想用 AliasMatch 替换以下内容：

```apache
Alias "/image/" "/ftp/pub/image/"
```

以下内容**不**等价——不要这样做！这会将所有任何位置包含 /image/ 的请求发送到 /ftp/pub/image/：

```apache
AliasMatch "/image/" "/ftp/pub/image/"
```

以下才是获得相同效果所需要的：

```apache
AliasMatch "^/image/(.*)$" "/ftp/pub/image/$1"
```

请求 URL 中的多个前导斜杠会在此模块的指令与请求 URL 路径进行比较之前被服务器丢弃。

### `<Location>` 指令 —— URL 指令区域块

https://httpd.apache.org/docs/2.4/en/mod/core.html#location

- 描述：仅将所包含的指令应用于匹配的 URL
- 语法：`<Location URL-path|URL> ... </Location>`
- 上下文：server config, virtual host
- 状态：Core
- 模块：core

`<Location>` 指令按 URL 限制所包含指令的作用域。它类似于 [`<Directory>`](#directory) 指令，并开始一个子部分，该子部分以 `</Location>` 指令终止。`<Location>` 部分按它们在配置文件中出现的顺序处理，在处理 [`<Directory>`](#directory) 部分和 `.htaccess` 文件之后，以及在 [`<Files>`](#files) 部分之后处理。

`<Location>` 部分完全在文件系统之外运作。这有几个后果。最重要的是，`<Location>` 指令不应用于控制对文件系统位置的访问。由于多个不同的 URL 可能映射到同一个文件系统位置，此类访问控制可能会被绕过。

如果 URL 的路径组件满足以下**任一**条件，则所包含的指令将应用于该请求：

- 指定的 location 与 URL 的路径组件完全匹配。
- 指定的 location（以正斜杠结尾）是 URL 路径组件的前缀（被视为上下文根）。
- 指定的 location 加上尾部斜杠后，是 URL 路径组件的前缀（也被视为上下文根）。

在下面的示例中，未使用尾部斜杠，对 /private1、/private1/ 和 /private1/file.txt 的请求将应用所包含的指令，但 /private1other 不会。

```apache
<Location "/private1">
    #  ...
</Location>
```

在下面的示例中，使用了尾部斜杠，对 /private2/ 和 /private2/file.txt 的请求将应用所包含的指令，但 /private2 和 /private2other 不会。

```apache
<Location "/private2/">
    # ...
</Location>
```

> **何时使用 `<Location>`**
>
> 使用 `<Location>` 将指令应用于存在于文件系统之外的内容。对于存在于文件系统中的内容，请使用 [`<Directory>`](#directory) 和 [`<Files>`](#files)。一个例外是 `<Location "/">`，它是将配置应用于整个服务器的简便方法。

- 对于所有源（非代理）请求，要匹配的 URL 是形式为 `/path/` 的 URL 路径。**不得包含方案、主机名、端口或查询字符串。** 

- 对于代理请求，要匹配的 URL 取决于代理的类型。

- 对于**正向**代理（[`ProxyRequests`](../mod/mod_proxy.html#proxyrequests)），要匹配的 URL 形式为 `scheme://servername/path`，你必须包含前缀。

- 对于**反向**代理（通过 [`ProxyPass`](../mod/mod_proxy.html#proxypass) 或 [`RewriteRule ... [P]`](../mod/mod_proxy.html#rewriterule ... [p]) 配置），请求以本地 URL 路径形式到达，因此就像源请求一样使用 `/path/`。

URL 可以使用通配符。在通配符字符串中，`?` 匹配任何单个字符，`*` 匹配任何字符序列。两个通配符都不匹配 URL 路径中的 /。

也可以使用[正则表达式](https://httpd.apache.org/docs/current/glossary.html#regex)，只需添加 `~` 字符。例如：

```apache
<Location ~ "/(extra|special)/data">
    #...
</Location>
```

这将匹配包含子字符串 `/extra/data` 或 `/special/data` 的 URL。指令 [`<LocationMatch>`](#locationmatch) 的行为与 `<Location>` 的正则表达式版本相同，并且更受推荐，原因很简单：在许多字体中 `~` 难以与 `-` 区分。

`<Location>` 功能在与 [`SetHandler`](#sethandler) 指令结合使用时特别有用。例如，要启用状态请求但仅允许来自 `example.com` 的浏览器，使用：

```apache
<Location "/status">
  SetHandler server-status
  Require host example.com
</Location>
```

> **关于 /（斜杠）的说明**
>
> 斜杠字符根据其在 URL 中出现的位置具有特殊含义。人们可能习惯了它在文件系统中的行为，即多个相邻斜杠经常被折叠为单个斜杠（*即*，`/home///foo` 与 `/home/foo` 相同）。在 URL 空间中，如果指令 [`MergeSlashes`](#mergeslashes) 已设置为 "OFF"，这不一定成立。[`<LocationMatch>`](#locationmatch) 指令和 `<Location>` 的正则表达式版本要求你在斜杠未被合并时显式指定多个斜杠。
>
> 例如，`<LocationMatch "^/abc">` 将匹配请求 URL `/abc`，但不匹配请求 URL `//abc`。（非正则）`<Location>` 指令在用于代理请求时行为类似。但是当（非正则）`<Location>` 用于非代理请求时，它会隐式地将多个斜杠与单个斜杠匹配。例如，如果你指定 `<Location "/abc/def">` 而请求是 `/abc//def`，则它会匹配。

#### 另请参阅

- [`<Directory>`、`<Location>` 和 `<Files>` 部分如何工作](../sections.html)，以解释收到请求时这些不同部分如何组合。
- [`LocationMatch`](#locationmatch)


### Apache Module mod_proxy

https://httpd.apache.org/docs/current/mod/mod_proxy.html

#### ProxyPass Directive 

https://httpd.apache.org/docs/current/mod/mod_proxy.html#proxypass

此指令允许将远程服务器映射到本地服务器的空间中。本地服务器并不以传统意义上的代理方式运作，而是表现为远程服务器的一个镜像。本地服务器通常被称为**反向代理**或**网关**。*path* 是本地虚拟路径的名称；*url* 是远程服务器的部分 URL，不能包含查询字符串。

Worker|BalancerMember parameters

Parameter 	Default 	Description

- `disablereuse`（`Off`）
  当你希望强制 mod_proxy 在使用后立即关闭与后端的连接，从而对该后端禁用其持久连接和连接池时，应使用此参数。这有助于在 Apache httpd 与后端服务器（无论协议如何）之间的防火墙倾向于静默丢弃连接，或后端本身可能处于轮询 DNS 下的各种情况。当启用连接复用时，每个后端域在每个子进程中仅解析一次（通过 DNS 查询），并为所有后续连接缓存，直到子进程被回收。要禁用连接复用，请将此属性值设置为 `On`。

- `keepalive`（`Off`）
  当你的 Apache httpd 与后端服务器之间有防火墙，且该防火墙倾向于丢弃非活动连接时，应使用此参数。此标志将告知操作系统在非活动连接上发送 `KEEP_ALIVE` 消息，从而防止防火墙丢弃连接。要启用 keepalive，请将此属性值设置为 `On`。

  初始和后续 TCP keepalive 探测的频率取决于操作系统的全局设置，可能高达 2 小时。为了使其有用，操作系统中配置的频率必须小于防火墙使用的阈值。