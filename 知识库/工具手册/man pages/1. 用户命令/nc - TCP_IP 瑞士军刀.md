https://manpages.debian.org/trixie/netcat-traditional/nc.1.en.html

# `nc` - `TCP/IP` 瑞士军刀

## 概要

```sh
nc [-46bCDdFhklNnrStUuvZz]
   [-I length]
   [-i interval]
   [-M ttl]
   [-m minttl]
   [-O length]
   [-P proxy_username]
   [-p source_port]
   [-q seconds]
   [-s sourceaddr]
   [-T keyword]
   [-V rtable]
   [-W recvlimit]
   [-w timeout]
   [-X proxy_protocol]
   [-x proxy_address[:port]]
   [destination] [port]
```

## 描述

`nc`（或 `netcat`）实用程序可用于几乎所有涉及 TCP、UDP 或 UNIX 域套接字的事情。它可以打开 TCP 连接、发送 UDP 数据包、监听任意 TCP 和 UDP 端口、进行端口扫描，并同时处理 IPv4 和 IPv6。与 [telnet(1)] 不同，`nc` 可以很好地编写脚本，并将错误消息分离到标准错误，而不是像 [telnet(1)] 对某些情况那样发送到标准输出。

常见用途包括：

- 简单的 TCP 代理
- 基于 shell 脚本的 HTTP 客户端和服务器
- 网络守护进程测试
- 用于 [ssh(1)] 的 SOCKS 或 HTTP `ProxyCommand`
- 以及更多更多

选项如下：

- `-4`  
    仅使用 IPv4 地址。

- `-6`  
    仅使用 IPv6 地址。

- `-b`  
    允许广播。

- `-C`  
    发送 CRLF 作为行结束符。输入数据中的每个换行（LF）字符在写入套接字之前都会转换为 CR+LF。已经以回车（CR）开头的换行字符不会被转换。接收到的数据不受影响。

- `-D`  
    在套接字上启用调试。

- `-d`  
    不要尝试从 stdin 读取。

- `-F`  
    使用 [sendmsg(2)] 将第一个已连接的套接字传递到标准输出并退出。这与 `-X` 结合使用时很有用，可让 `nc` 通过代理执行连接设置，然后将连接的其余部分留给另一个程序（例如使用 [ssh_config(5)] 的 `ProxyUseFdpass` 选项的 [ssh(1)]）。不能与 `-U` 一起使用。

- `-h`  
    打印 `nc` 帮助文本并退出。

- `-I length`  
    指定 TCP 接收缓冲区的大小。

- `-i interval`  
    在发送和接收的每行文本之间休眠 `interval` 秒。还会导致连接到多个端口之间的延迟时间。

- `-k`  
    当连接完成后，继续监听另一个连接。需要 `-l`。与 `-u` 选项一起使用时，服务器套接字不会连接，并且可以接收来自多个主机的 UDP 数据报。

- `-l`  
    监听传入连接，而不是向远程主机发起连接。要监听的 `destination` 和 `port` 可以指定为非可选参数，也可以分别使用 `-s` 和 `-p` 选项指定。不能与 `-x` 或 `-z` 一起使用。此外，使用 `-w` 选项指定的任何超时都会被忽略。

- `-M ttl`  
    设置传出数据包的 TTL / 跳数限制。

- `-m minttl`  
    要求内核丢弃 TTL / 跳数限制低于 `minttl` 的传入数据包。

- `-N`  
    在输入遇到 EOF 后对网络套接字执行 [shutdown(2)]。某些服务器需要这样做才能完成它们的工作。

- `-n`  
    不执行域名解析。如果名称无法在不使用 DNS 的情况下解析，则会报告错误。

- `-O length`  
    指定 TCP 发送缓冲区的大小。

- `-P proxy_username`  
    指定向需要身份验证的代理服务器提供的用户名。如果未指定用户名，则不会尝试身份验证。目前仅 `HTTP CONNECT` 代理支持代理身份验证。

- `-p source_port`  
    指定 `nc` 应使用的源端口，受权限限制和可用性约束。

- `-q seconds`  
    在 `stdin` 上遇到 `EOF` 后，等待指定的 `seconds` 秒然后退出。如果 `seconds` 为负，则永远等待（默认）。指定非负的 `seconds` 隐含 `-N`。

- `-r`  
    在范围内随机选择源端口和/或目标端口，而不是按顺序选择，或按系统分配它们的顺序选择。

- `-S`  
    启用 RFC 2385 TCP MD5 签名选项。

- `-s sourceaddr`  
    设置发送数据包的源地址，这在具有多个接口的机器上很有用。对于 UNIX 域数据报套接字，指定要创建和使用的本地临时套接字文件，以便可以接收数据报。不能与 `-x` 一起使用。

- `-T keyword`  
    更改 IPv4 TOS/IPv6 流量类别值。`keyword` 可以是 `critical`、`inetcontrol`、`lowcost`、`lowdelay`、`netcontrol`、`throughput`、`reliability` 之一，也可以是 DiffServ 代码点之一：`ef`、`af11` ... `af43`、`cs0` ... `cs7`；或者十六进制或十进制数字。

- `-t`  
    向 RFC 854 `DO` 和 `WILL` 请求发送 RFC 854 `DON'T` 和 `WON'T` 响应。这使得可以使用 `nc` 编写 `telnet` 会话脚本。

- `-U`  
    使用 UNIX 域套接字。不能与 `-F` 或 `-x` 一起使用。在 Linux 上，如果名称以 at 符号（`@`）开头，则将其读取为抽象命名空间套接字：在绑定或连接之前，前导 `@` 会被替换为 **NUL** 字节。详情参见 [unix(7)]。

- `-u`  
    使用 UDP 而不是 TCP。不能与 `-x` 一起使用。对于 UNIX 域套接字，使用数据报套接字而不是流套接字。如果使用 UNIX 域套接字，除非给出 `-s` 标志，否则会在 `/tmp` 中创建临时接收套接字。

- `-V rtable`  
    设置要使用的路由表。

- `-v`  
    生成更详细的输出。

- `-W recvlimit`  
    从网络接收到 `recvlimit` 个数据包后终止。

- `-w timeout`  
    无法建立或空闲的连接在 `timeout` 秒后超时。`-w` 标志对 `-l` 选项没有影响，即无论是否带有 `-w` 标志，`nc` 都将永远监听连接。默认没有超时。

- `-X proxy_protocol`  
    与代理服务器通信时使用 `proxy_protocol`。支持的协议有 `4`（SOCKS v.4）、`4A`（SOCKS v.4A）、`5`（SOCKS v.5）和 `connect`（HTTPS 代理）。如果未指定协议，则使用 SOCKS 版本 5。请注意，SOCKS v.4 协议非常有限，只能在目标主机可解析为 IPv4 地址时使用。其他协议将目标作为字符串传递给远程代理进行解释，没有此限制。

- `-x proxy_address[:port]`  
    使用 `proxy_address` 和 `port` 处的代理连接到 `destination`。如果未指定 `port`，则使用代理协议的知名端口（SOCKS 为 1080，HTTPS 为 3128）。可以通过将 `proxy_address` 括在方括号中来明确指定 IPv6 地址。代理不能与 `-lsuU` 中的任何选项一起使用。

- `-Z`  
    DCCP 模式。

- `-z`  
    仅扫描监听守护进程，不向它们发送任何数据。不能与 `-l` 一起使用。

`destination` 可以是数字 IP 地址或符号主机名（除非给出 `-n` 选项）。通常必须指定目标，除非给出 `-l` 选项（此时使用本地主机）。对于 UNIX 域套接字，目标是必需的，并且是要连接（如果给出 `-l` 选项，则监听）的套接字路径。

`port` 可以指定为数字端口号或服务名。端口范围可以指定为 `nn`-`mm` 形式的数字端口号。通常必须指定目标端口，除非给出 `-U` 选项。对于某些选项，值 0 请求系统选择端口号。

## 客户端/服务器模型

使用 `nc` 构建非常基本的客户端/服务器模型非常简单。在一个控制台上，启动 `nc` 监听特定端口以等待连接。例如：

```console
$ nc -l 1234
```

`nc` 现在正在端口 1234 上监听连接。在第二个控制台（或第二台机器）上，连接到正在监听的机器和端口：

```console
$ nc -N 127.0.0.1 1234
```

现在应该已在端口之间建立连接。在第二个控制台输入的任何内容都将连接到第一个控制台，反之亦然。连接建立后，`nc` 并不真正关心哪一侧用作“服务器”，哪一侧用作“客户端”。由于给出了 `-N` 标志，可以使用 `EOF`（`^D`）终止连接。

此 netcat 没有 `-c` 或 `-e` 选项，但仍可以通过重定向文件描述符在连接建立后执行命令。请谨慎操作，因为打开端口并允许任何连接者在您的站点上执行任意命令是危险的。如果确实需要这样做，这里有一个示例：

在“服务器”侧：

```console
$ rm -f /tmp/f; mkfifo /tmp/f
$ cat /tmp/f | /bin/sh -i 2>&1 | nc -l 127.0.0.1 1234 > /tmp/f
```

在“客户端”侧：

```console
$ nc host.example.com 1234
```

```log
$ (shell prompt from host.example.com)
```

通过这样做，您在 `/tmp/f` 创建了一个 fifo，并让 `nc` 在“服务器”侧的地址 `127.0.0.1` 的端口 1234 上监听；当“客户端”成功建立到该端口的连接时，`/bin/sh` 会在“服务器”侧执行，并将 shell 提示符提供给“客户端”侧。

连接终止时，`nc` 也会退出。如果希望它继续监听，请使用 `-k`，但如果命令退出，此选项不会重新启动它或保持 `nc` 运行。另外，不再需要文件描述符后，别忘了删除它：

```console
$ rm -f /tmp/f
```

## 数据传输

上一节中的示例可以扩展为构建基本的数据传输模型。输入到连接一端的信息将输出到另一端，并且可以轻松捕获输入和输出以模拟文件传输。

首先使用 `nc` 监听特定端口，并将输出捕获到文件中：

```console
$ nc -l 1234 > filename.out
```

使用第二台机器连接到正在监听的 `nc` 进程，并向其提供要传输的文件：

```console
$ nc -N host.example.com 1234 < filename.in
```

文件传输完成后，连接将自动关闭。

## 与服务器通信

有时“手动”与服务器通信而不是通过用户界面会很有用。它有助于故障排除，例如在需要验证服务器响应客户端发出的命令而发送什么数据时。例如，要检索网站的主页：

```console
$ printf "GET / HTTP/1.0\r\n\r\n" | nc host.example.com 80
```

请注意，这也会显示 Web 服务器发送的标头。如有必要，可以使用 [sed(1)] 等工具过滤它们。

当用户知道服务器所需请求的格式时，可以构建更复杂的示例。再例如，可以使用以下方式向 SMTP 服务器提交电子邮件：

```console
$ nc [-C] localhost 25 << EOF
HELO host.example.com
MAIL FROM:<user@host.example.com>
RCPT TO:<user2@host.example.com>
DATA
Body of email.
.
QUIT
EOF
```

## 端口扫描

了解目标机器上哪些端口开放并运行服务可能很有用。`-z` 标志可用于告诉 `nc` 报告开放端口，而不是发起连接。通常，将其与 `-v` 选项一起使用以通过标准错误打开详细输出会很有用。

例如：

```console
$ nc -zv host.example.com 20-30
Connection to host.example.com 22 port [tcp/ssh] succeeded!
Connection to host.example.com 25 port [tcp/smtp] succeeded!
```

指定端口范围以将搜索限制在端口 20 - 30，并按递增顺序扫描（除非设置了 `-r` 标志）。

您还可以指定要扫描的端口列表，例如：

```console
$ nc -zv host.example.com http 20 22-23
nc: connect to host.example.com 80 (tcp) failed: Connection refused
nc: connect to host.example.com 20 (tcp) failed: Connection refused
Connection to host.example.com port [tcp/ssh] succeeded!
nc: connect to host.example.com 23 (tcp) failed: Connection refused
```

端口按您给出的顺序扫描（除非设置了 `-r` 标志）。

另外，了解正在运行哪个服务器软件以及哪个版本可能很有用。此信息通常包含在问候横幅中。为了检索这些信息，有必要先建立连接，然后在检索到横幅后断开连接。这可以通过使用 `-w` 标志指定较短的超时，或者向服务器发出 `QUIT` 命令来实现：

```console
$ echo "QUIT" | nc host.example.com 20-30
SSH-1.99-OpenSSH_3.6.1p2
Protocol mismatch.
220 host.example.com IMS SMTP Receiver Version 0.84 Ready
```

## 示例

打开到 host.example.com 端口 42 的 TCP 连接，使用端口 31337 作为源端口，超时为 5 秒：

```console
$ nc -p 31337 -w 5 host.example.com 42
```

打开到 host.example.com 端口 53 的 UDP 连接：

```console
$ nc -u host.example.com 53
```

打开到 host.example.com 端口 42 的 TCP 连接，并使用 10.1.2.3 作为连接本地端的 IP：

```console
$ nc -s 10.1.2.3 host.example.com 42
```

创建并监听一个 UNIX 域流套接字：

```console
$ nc -lU /var/tmp/dsocket
```

通过位于 10.2.3.4、端口 8080 的 HTTP 代理连接到 host.example.com 的端口 42。此示例也可供 [ssh(1)] 使用；更多信息参见 [ssh_config(5)] 中的 `ProxyCommand` 指令。

```console
$ nc -x10.2.3.4:8080 -Xconnect host.example.com 42
```

同一个示例，这次如果代理要求，则使用用户名“ruser”启用代理身份验证：

```console
$ nc -x10.2.3.4:8080 -Xconnect -Pruser host.example.com 42
```

## 另请参阅

[cat(1)]、[ssh(1)]

## 作者

原始实现由 *Hobbit* <[hobbit@avian.org](mailto:hobbit@avian.org)>。由 Eric Jackson <[ericj@monkey.org](mailto:ericj@monkey.org)> 重写并加入 IPv6 支持。由 Aron Xu ⟨[aron@debian.org](mailto:aron@debian.org)⟩ 修改为 Debian 移植版本。

## 注意事项

使用 `-uz` 标志组合进行 UDP 端口扫描时，无论目标机器状态如何，都会始终报告成功。但是，结合目标机器或中间设备上的流量嗅探器，`-uz` 组合可能对通信诊断有用。请注意，生成的 UDP 流量量可能因硬件资源和/或配置设置而受到限制。