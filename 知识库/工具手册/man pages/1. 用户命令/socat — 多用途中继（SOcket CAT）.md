https://www.man7.org/linux/man-pages/man1/socat.1.html

未包含章节
- ADDRESS OPTIONS
- DATA VALUES

# `socat` — 多用途中继（SOcket CAT）

## 概要

```sh
socat [options] <address> <address>
socat -V
socat -h[h[h]] | -?[?[?]]
filan
procan
```

## 描述

`socat` 是一个基于命令行的实用程序，它建立两个双向字节流，并在它们之间传输数据。由于这些流可以由大量不同类型的数据接收器和数据源（参见地址类型）构造，并且可以对这些流应用许多地址选项，因此 `socat` 可用于许多不同目的。

`Filan` 是一个实用程序，它将有关其活动文件描述符的信息打印到 `stdout`。它编写用于调试 `socat`，但也可能对其他目的有用。使用 `-h` 选项查找更多信息。

`Procan` 是一个实用程序，它将有关进程参数的信息打印到 `stdout`。它编写用于更好地理解某些 UNIX 进程属性并用于调试 `socat`，但也可能对其他目的有用。

`socat` 实例的生命周期通常由四个阶段组成。

在 `init` 阶段，解析命令行选项并初始化日志记录。

在 `open` 阶段，`socat` 打开第一个地址，然后打开第二个地址。这些步骤通常是阻塞的；因此，特别是对于像 `socks` 这样的复杂地址类型，连接请求或身份验证对话框必须在下一步开始之前完成。

在 `transfer` 阶段，`socat` 通过 `select()` 监视两个流的读取和写入文件描述符，并且当一侧有数据可用并且可以写入另一侧时，`socat` 读取它，执行所需的换行符转换，并将数据写入另一个流的写入文件描述符，然后继续等待两个方向上的更多数据。

当其中一个流有效到达 `EOF` 时，`closing` 阶段开始。`socat` 将 `EOF` 条件传输到另一个流，即尝试仅关闭其写入流，给它一个优雅终止的机会。在定义的时间内，`socat` 继续在另一个方向传输数据，但随后关闭所有剩余通道并终止。

## 选项

`socat` 提供一些命令行选项来修改程序的行为。它们与所谓地址选项无关，地址选项用作地址规范的一部分。

- `-V`  
    将版本和可用特性信息打印到 `stdout`，然后退出。

- `-h | -?`  
    将描述命令行选项和可用地址类型的帮助文本打印到 `stdout`，然后退出。

- `-hh | -??`  
    类似 `-h`，外加所有可用地址选项短名称的列表。某些选项依赖于平台，因此此输出有助于检查特定实现。

- `-hhh | -???`  
    类似 `-hh`，外加所有可用地址选项名称的列表。

- `-d`  
    不使用此选项时，只打印致命、错误和警告消息；应用此选项还会打印通知消息。更多信息请参见“诊断”。

- `-d0`  
    使用此选项时，只打印致命和错误消息；这恢复 `socat` 直到 1.7.4 版本的行为。

- `-d -d | -dd | -d2`  
    打印致命、错误、警告和通知消息。

- `-d -d -d | -ddd | -d3`  
    打印致命、错误、警告、通知和信息消息。

- `-d -d -d -d | -dddd | -d4`  
    打印致命、错误、警告、通知、信息和调试消息。

- `-D`  
    在开始传输阶段之前记录有关文件描述符的信息。

- `--experimental`  
    未充分测试或将来可能更改的新特性必须使用此选项显式启用。

- `-ly[<facility>]`  
    将消息写入 `syslog` 而不是 `stderr`；严重性由 `-d` 选项定义。使用可选 `<facility>` 可以选择 `syslog` 类型，默认是 `daemon`。第三方库可能不遵守此选项。

- `-lf <logfile>`  
    将消息写入 `<logfile>` [文件名] 而不是 `stderr`。某些第三方库，特别是 `libwrap`，可能不遵守此选项。

- `-ls`  
    将消息写入 `stderr`（这是默认值）。某些第三方库可能不遵守此选项，特别是 `libwrap` 似乎只记录到 `syslog`。

- `-lp<progname>`  
    覆盖错误消息中打印的程序名，以及用于构造环境变量名的程序名。

- `-lu`  
    将错误消息的时间戳扩展到微秒分辨率。记录到 `syslog` 时不起作用。

- `-lm[<facility>]`  
    混合日志模式。启动期间消息打印到 `stderr`；当 `socat` 启动传输阶段循环或守护进程模式时（即打开所有流之后、开始数据传输之前，或者对于带 `fork` 选项的监听套接字，在第一次 `accept` 调用之前），它将日志记录切换到 `syslog`。使用可选 `<facility>` 可以选择 `syslog` 类型，默认是 `daemon`。

- `-lh`  
    向日志消息添加主机名。使用环境变量 `HOSTNAME` 的值，如果未设置 `HOSTNAME`，则使用通过 `uname()` 获取的值。

- `-v`  
    将传输的数据不仅写入其目标流，还写入 `stderr`。输出格式为文本，并带有一些便于阅读的转换，前缀为 `> ` 或 `< ` 表示流向。

- `-x`  
    将传输的数据不仅写入其目标流，还写入 `stderr`。输出格式为十六进制，前缀为 `> ` 或 `< ` 表示流向。可与 `-v` 组合使用。

- `-r <file>`  
    将从左地址流向右地址的原始（二进制）数据转储到给定文件。文件名可以包含对环境变量的引用以及 `$$`（pid）、`$PROGNAME`（参见选项 `-lp`）、`$TIMESTAMP`（使用格式 `%Y%m%dT%H%M%S`）和 `MICROS`（一天中的微秒）。当然，这些引用必须防止 shell 展开。

- `-R <file>`  
    将从右地址流向左地址的原始（二进制）数据转储到给定文件。有关文件名自定义，请参见选项 `-r`。

- `-b<size>`  
    设置数据传输块 `<size>` [size_t]。每一步最多传输 `<size>` 字节。默认是 `8192` 字节。

- `-s`  
    默认情况下，发生错误时 `socat` 会终止，以防止在某个选项无法应用时进程继续运行。使用此选项时，`socat` 对错误较为宽松并尝试继续。即使使用此选项，`socat` 也会在致命错误时退出，并在安全检查失败时中止连接尝试。

- `-S<signals-bitmap>`  
    更改 `socat` 仅为了打印日志消息而捕获的信号集。这种捕获有助于将信号信息写入 `socat` 的日志，但会阻止核心转储或其他标准动作。这些信号的默认集合是 `SIGHUP`、`SIGINT`、`SIGQUIT`、`SIGILL`、`SIGABRT`、`SIGBUS`、`SIGFPE`、`SIGSEGV` 和 `SIGTERM`；用位图替换此集合（Linux 上为 `0x89de`）（例如，`SIGFPE` 的值为 8，其位为 `0x0080`）。  
    注意：信号 `SIGHUP`、`SIGINT`、`SIGQUIT`、`SIGUSR1`、`SIGPIPE`、`SIGALRM`、`SIGTERM` 和 `SIGCHLD` 可能无论如何都会被特殊处理。

- `-t<timeout>`  
    当一个通道到达 `EOF`（即未被选项 `ignoreeof` 忽略）时，另一个通道的写入部分被关闭。然后，`socat` 等待 `<timeout>` [timeval] 秒后终止。在超时间隔内，如果该另一个通道的读取部分给出 `EOF`，`socat` 会终止而不等待超时。默认是 `0.5` 秒，`0` 有效。此超时仅对写入和读取部分可以独立关闭或关闭的地址有用。

- `-T<timeout>`  
    总不活动超时：当 `socat` 已经进入传输循环，并且在 `<timeout>` [timeval] 秒内没有发生任何事情（没有数据到达，没有发生中断……）时，它终止。直到 1.8.0.0 版本，“0”表示“无限”；从 1.8.0.1 版本开始，“0”表示 0，小于 0 的值表示无限，默认是 `-1`。  
    对像 `UDP` 这样无法传输 `EOF` 的协议有用。

- `-u`  
    使用单向模式。第一个地址仅用于读取，第二个地址仅用于写入（示例）。

- `-U`  
    以相反方向使用单向模式。第一个地址仅用于写入，第二个地址仅用于读取。

- `-g`  
    在地址选项解析期间，不检查该选项在给定地址环境中是否被认为有用。如果你想强制将例如套接字选项应用于串行设备，请使用它。

- `-L<lockfile>`  
    如果 `lockfile` 存在，则报错退出。如果 `lockfile` 不存在，则创建它并继续，退出时删除 `lockfile`。

- `-W<lockfile>`  
    如果 `lockfile` 存在，则等待直到它消失。当 `lockfile` 不存在时，创建它并继续，退出时删除 `lockfile`。

- `-4`  
    在地址未隐式或显式指定版本的情况下使用 IP 版本 4。从 1.8.0.1 版本开始，这是默认值。

- `-6`  
    在地址未隐式或显式指定版本的情况下使用 IP 版本 6。

- `-0`  
    不偏好特定 IP 版本；这会让被动地址（`LISTEN`、`RECV` 等）在某些平台上同时服务两个版本（不是 BSD）。

- 
    ```
    --statistics
    -S
    ```
    在终止 `socat` 前记录传输统计信息（两个方向的字节和块计数器）。另请参阅信号 `USR1`。

## 地址规范

通过地址命令行参数，用户向 `socat` 提供建立字节流所需的指令和必要信息。

地址规范通常由地址类型关键字、零个或多个必需地址参数（用 `:` 与关键字以及彼此分隔）以及零个或多个地址选项（用 `,` 分隔）组成。

关键字指定地址类型（例如 `TCP4`、`OPEN`、`EXEC`）。某些关键字存在同义词（`-` 表示 `STDIO`，`TCP` 表示 `TCP4`）。关键字不区分大小写。对于少数特殊地址类型，可以省略关键字：以数字开头的地址规范被假定为 `FD`（原始文件描述符）地址；如果在第一个 `:` 或 `,` 之前找到 `/`，则假定为 `GOPEN`（通用文件打开）。

必需地址参数的数量和类型取决于地址类型。例如，`TCP4` 需要服务器规范（名称或地址）和端口规范（编号或服务名）。

每个地址可以给出零个或多个地址选项。它们以某种方式影响地址。选项由选项关键字或选项关键字和值组成，值用 `=` 分隔。选项关键字不区分大小写。为了筛选对地址类型有用的选项，每个选项属于一个选项组。对于每种地址类型，允许一组选项组。只有属于这些地址组之一的选项才可使用（使用选项 `-g` 时除外）。

遵循上述模式的地址规范也称为单地址规范。两个单地址可以用 `!!` 组合，形成一个通道的双类型地址。这里，第一个地址由 `socat` 用于读取数据，第二个地址用于写入数据。无法只指定一次选项并将其同时应用于两个单地址。

通常，地址以读/写模式打开。当地址是双地址规范的一部分，或使用选项 `-u` 或 `-U` 时，地址可能仅用于读取或仅用于写入。考虑这一点对于某些地址类型很重要。

从 `socat` 1.5.0 及更高版本开始，词法分析尝试有意义地处理引号和括号，并允许转义特殊字符。如果找到字符 `{`、`[`、`'` 之一，则查找相应的结束字符 `}`、`]`、`'`；它们也可以嵌套。在这些结构内，`socat` 的特殊字符和字符串 `:`、`,`、`!!` 不会被特殊处理。所有这些字符和字符串都可以用 `\` 或在 `""` 内转义。

## 地址类型

本节描述可用的地址类型及其关键字、参数和语义。

### `CREATE:<filename>`

```
CREATE:<filename>
```

使用 `creat()` 打开 `<filename>`，并将文件描述符用于写入。这是只写地址，因为用 `creat` 打开的文件无法读取。请参见选项 `-u` 和 `-U`，以及双地址。  
像 `O_LARGEFILE` 这样的标志无法应用。如果需要它们，请使用 `OPEN` 并配合选项 `create`、`create`。  
`<filename>` 必须是有效存在或不存在的路径。如果 `<filename>` 是命名管道，`creat()` 可能会阻塞；如果 `<filename>` 引用套接字，这是错误。  
选项组：`FD`、`REG`、`NAMED`  
有用选项：`mode`、`mode`、`user`、`group`、`unlink-early`、`unlink-late`、`append`  
另请参阅：`OPEN`、`GOPEN`

### `DCCP-CONNECT:<host>:<port> (DCCP:<host>:<port>)`

```
DCCP-CONNECT:<host>:<port> (DCCP:<host>:<port>)
```

建立到指定 `<host>` [IP 地址] 和 `<port>` [DCCP 服务] 的 DCCP 连接，根据地址规范、名称解析或选项 `pf` 使用 IP 版本 4 或 6。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`SCTP`、`CHILD`、`RETRY`  
有用选项：`bind`、`connect-timeout`、`tos`、`dccp-set-ccid`、`nonblock`、`sourceport`、`retry`、`readbytes`  
另请参阅：`DCCP4-CONNECT`、`DCCP6-CONNECT`、`DCCP-LISTEN`、`TCP-CONNECT`、`SCTP-CONNECT`

### `DCCP4-CONNECT:<host>:<port> (DCCP4:<host>:<port>)`

```
DCCP4-CONNECT:<host>:<port> (DCCP4:<host>:<port>)
```

类似 `DCCP-CONNECT`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`、`DCCP`、`CHILD`、`RETRY`

### `DCCP6-CONNECT:<host>:<port> (DCCP6:<host>:<port>)`

```
DCCP6-CONNECT:<host>:<port> (DCCP6:<host>:<port>)
```

类似 `DCCP-CONNECT`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`DCCP`、`CHILD`、`RETRY`

### `DCCP-LISTEN:<port> (DCCP-L:<port>)`

```
DCCP-LISTEN:<port> (DCCP-L:<port>)
```

在 `<port>` [DCCP 服务] 上监听并接受 DCCP 连接。IP 版本为 4，或由地址选项 `pf`、`socat` 选项（`-4`、`-6`）或环境变量 `SOCAT_DEFAULT_LISTEN_IP` 指定。注意，打开此地址通常会阻塞直到客户端连接。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`IP6`、`DCCP`、`RETRY`  
有用选项：`fork`、`bind`、`range`、`max-children`、`backlog`、`accept-timeout`、`dccp-set-sid`、`su`、`reuseaddr`、`retry`  
另请参阅：`DCCP4-LISTEN`、`DCCP6-LISTEN`、`TCP-LISTEN`、`SCTP-LISTEN`、`DCCP-CONNECT`

### `DCCP4-LISTEN:<port> (DCCP4-L:<port>)`

```
DCCP4-LISTEN:<port> (DCCP4-L:<port>)
```

类似 `DCCP-LISTEN`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`DCCP`、`RETRY`

### `DCCP6-LISTEN:<port> (DCCP6-L:<port>)`

```
DCCP6-LISTEN:<port> (DCCP6-L:<port>)
```

类似 `DCCP-LISTEN`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP6`、`DCCP`、`RETRY`

### `EXEC:<command-line>`

```
EXEC:<command-line>
```

派生一个子进程，使其与父进程建立通信，并使用 `execvp()` 调用指定程序。`<command-line>` 是简单命令，参数由单个空格分隔。如果程序名包含 `/`，最后一个 `/` 之后的部分作为 `ARGV[0]`。如果程序名是相对路径，则适用 `execvp()` 通过 `$PATH` 查找程序的语义。程序成功启动后，`socat` 将数据写入进程的 `stdin`，并从其 `stdout` 读取；默认使用由 `socketpair()` 生成的 UNIX 域套接字。（示例）  
选项组：`FD`、`SOCKET`、`EXEC`、`FORK`、`TERMIOS`  
有用选项：`path`、`fdin`、`fdout`、`chroot`、`su`、`su-d`、`nofork`、`socktype`、`pty`、`stderr`、`ctty`、`setsid`、`pipes`、`umask`、`login`、`sigint`、`sigquit`、`netns`  
另请参阅：`SYSTEM`、`SHELL`

### `FD:<fdnum>`

```
FD:<fdnum>
```

使用文件描述符 `<fdnum>`。它必须已经作为有效的 UN*X 文件描述符存在。  
选项组：`FD`（`TERMIOS`、`REG`、`SOCKET`）  
另请参阅：`STDIO`、`STDIN`、`STDOUT`、`STDERR`

### `GOPEN:<filename>`

```
GOPEN:<filename>
```

（通用打开）此地址类型尝试以有用的方式处理除目录之外的任何文件系统条目。`<filename>` 可以是相对或绝对路径。如果它已存在，则检查其类型。如果是 UNIX 域套接字，`socat` 连接；如果连接失败，`socat` 假定是数据报套接字并使用 `sendto()` 调用。如果该条目不是套接字，`socat` 使用 `O_APPEND` 标志打开它。如果它不存在，则使用 `O_CREAT` 标志作为常规文件打开（示例）。  
选项组：`FD`、`REG`、`SOCKET`、`NAMED`、`OPEN`  
另请参阅：`OPEN`、`CREATE`、`UNIX-CONNECT`

### `IP-SENDTO:<host>:<protocol>`

```
IP-SENDTO:<host>:<protocol>
```

打开原始 IP 套接字。根据主机规范或选项 `pf`，使用 IP 协议版本 4 或 6。它使用 `<protocol>` 向 `<host>` [IP 地址] 发送数据包，并接收来自该主机的数据包，忽略来自其他主机的数据包。协议 `255` 使用原始套接字，其中 IP 头是数据的一部分。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`  
有用选项：`pf`、`ttl`  
另请参阅：`IP4-SENDTO`、`IP6-SENDTO`、`IP-RECVFROM`、`IP-RECV`、`UDP-SENDTO`、`UNIX-SENDTO`

### `INTERFACE:<interface>`

```
INTERFACE:<interface>
```

使用包括链路层数据的原始数据包与连接到某个接口的网络通信。`<interface>` 是网络接口的名称。目前仅在 Linux 上可用。  
选项组：`FD`、`SOCKET`  
有用选项：`pf`、`type`  
另请参阅：`ip-recv`

### `IP4-SENDTO:<host>:<protocol>`

```
IP4-SENDTO:<host>:<protocol>
```

类似 `IP-SENDTO`，但始终使用 IPv4。  
选项组：`FD`、`SOCKET`、`IP4`

### `IP6-SENDTO:<host>:<protocol>`

```
IP6-SENDTO:<host>:<protocol>
```

类似 `IP-SENDTO`，但始终使用 IPv6。  
选项组：`FD`、`SOCKET`、`IP6`

### `IP-DATAGRAM:<address>:<protocol>`

```
IP-DATAGRAM:<address>:<protocol>
```

将传出数据发送到指定地址，该地址尤其可以是广播或多播地址。到达本地套接字的数据包会检查其源地址是否匹配 `RANGE` 或 `TCPWRAP` 选项。此地址类型例如可用于实现对称或非对称广播或多播通信。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`RANGE`  
有用选项：`bind`、`range`、`tcpwrap`、`broadcast`、`ip-multicast-loop`、`ip-multicast-ttl`、`ip-multicast-if`、`ip-add-membership`、`ip-add-source-membership`、`ipv6-join-group`、`ipv6-join-source-group`、`ttl`、`tos`、`pf`  
另请参阅：`IP4-DATAGRAM`、`IP6-DATAGRAM`、`IP-SENDTO`、`IP-RECVFROM`、`IP-RECV`、`UDP-DATAGRAM`

### `IP4-DATAGRAM:<host>:<protocol>`

```
IP4-DATAGRAM:<host>:<protocol>
```

类似 `IP-DATAGRAM`，但始终使用 IPv4。（示例）  
选项组：`FD`、`SOCKET`、`IP4`、`RANGE`

### `IP6-DATAGRAM:<host>:<protocol>`

```
IP6-DATAGRAM:<host>:<protocol>
```

类似 `IP-DATAGRAM`，但始终使用 IPv6。请注意，IPv6 不支持广播。  
选项组：`FD`、`SOCKET`、`IP6`、`RANGE`

### `IP-RECVFROM:<protocol>`

```
IP-RECVFROM:<protocol>
```

打开 `<protocol>` 的原始 IP 套接字。根据选项 `pf`，使用 IP 协议版本 4 或 6。它从未指定的对等方接收一个数据包，并可以向该对等方发送一个或多个应答数据包。此模式在配合 `fork` 选项时特别有用，其中每个到达的数据包（来自任意对等方）由自己的子进程处理。这允许类似典型基于 UDP 的服务器（如 `ntpd` 或 `named`）的行为。  
请注意，当发送方和接收方 IP 地址相同时，应答数据包可能会被当作传入流量获取，因为没有端口号来区分套接字。  
此地址与 `IP-SENDTO` 地址对等方配合良好（见上文）。协议 `255` 使用原始套接字，其中 IP 头是数据的一部分。  
请参阅关于 `RECVFROM` 地址的说明。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`CHILD`、`RANGE`  
有用选项：`pf`、`fork`、`range`、`ttl`、`broadcast`  
另请参阅：`IP4-RECVFROM`、`IP6-RECVFROM`、`IP-SENDTO`、`IP-RECV`、`UDP-RECVFROM`、`UNIX-RECVFROM`

### `IP4-RECVFROM:<protocol>`

```
IP4-RECVFROM:<protocol>
```

类似 `IP-RECVFROM`，但始终使用 IPv4。  
选项组：`FD`、`SOCKET`、`IP4`、`CHILD`、`RANGE`

### `IP6-RECVFROM:<protocol>`

```
IP6-RECVFROM:<protocol>
```

类似 `IP-RECVFROM`，但始终使用 IPv6。  
选项组：`FD`、`SOCKET`、`IP6`、`CHILD`、`RANGE`

### `IP-RECV:<protocol>`

```
IP-RECV:<protocol>
```

打开 `<protocol>` 的原始 IP 套接字。根据选项 `pf`，使用 IP 协议版本 4 或 6。它从多个未指定的对等方接收数据包并合并数据。不可能回复；这是只读地址，请参见选项 `-u` 和 `-U`，以及双地址。例如，它可以由 `socat` 的 `IP-SENDTO` 地址对等方寻址。协议 `255` 使用原始套接字，其中 IP 头是数据的一部分。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`RANGE`  
有用选项：`pf`、`range`  
另请参阅：`IP4-RECV`、`IP6-RECV`、`IP-SENDTO`、`IP-RECVFROM`、`UDP-RECV`、`UNIX-RECV`

### `IP4-RECV:<protocol>`

```
IP4-RECV:<protocol>
```

类似 `IP-RECV`，但始终使用 IPv4。  
选项组：`FD`、`SOCKET`、`IP4`、`RANGE`

### `IP6-RECV:<protocol>`

```
IP6-RECV:<protocol>
```

类似 `IP-RECV`，但始终使用 IPv6。  
选项组：`FD`、`SOCKET`、`IP6`、`RANGE`

### `OPEN:<filename>`

```
OPEN:<filename>
```

使用 `open()` 系统调用打开 `<filename>`（示例）。此操作在 UNIX 域套接字上失败。  
注意：此地址类型在双向模式下很少有用。  
选项组：`FD`、`REG`、`NAMED`、`OPEN`  
有用选项：`creat`、`excl`、`noatime`、`nofollow`、`append`、`rdonly`、`wronly`、`lock`、`readbytes`、`ignoreeof`  
另请参阅：`CREATE`、`GOPEN`、`UNIX-CONNECT`

### `OPENSSL:<host>:<port>`

```
OPENSSL:<host>:<port>
```

尝试建立到 `<host>` [IP 地址] 上 `<port>` [TCP 服务] 的 SSL 连接，根据地址规范、名称解析或选项 `pf` 使用 TCP/IP 版本 4 或 6。  
注意：直到 1.7.2.4 版本，服务器证书仅根据系统证书存储、`cafile` 或 `capath` 检查有效性，而不检查与服务器名称或其 IP 地址的匹配。从 1.7.3.0 版本开始，`socat` 检查对等证书是否与 `<host>` 参数或 `openssl-commonname` 选项的值匹配。`socat` 尝试将其与证书的 subject commonName 以及证书扩展 subjectAltName DNS 名称匹配。支持证书中的通配符。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`OPENSSL`、`RETRY`  
有用选项：`min-proto-version`、`cipher`、`verify`、`commonname`、`cafile`、`capath`、`certificate`、`key`、`compress`、`bind`、`pf`、`connect-timeout`、`sourceport`、`retry`  
另请参阅：`OPENSSL-LISTEN`、`TCP`

### `OPENSSL-LISTEN:<port>`

```
OPENSSL-LISTEN:<port>
```

在 TCP `<port>` [TCP 服务] 上监听。IP 版本为 4，或由 `pf` 指定。当连接被接受时，此地址表现为 SSL 服务器。  
注意：你可能希望对此地址使用 `certificate` 选项。  
注意：客户端证书仅根据 `cafile` 或 `capath` 检查有效性，而不检查与客户端名称或其 IP 地址的匹配！  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`LISTEN`、`OPENSSL`、`CHILD`、`RANGE`、`RETRY`  
有用选项：`pf`、`min-proto-version`、`cipher`、`verify`、`commonname`、`cafile`、`capath`、`certificate`、`key`、`compress`、`fork`、`bind`、`range`、`tcpwrap`、`su`、`reuseaddr`、`retry`  
另请参阅：`OPENSSL`、`TCP-LISTEN`

### `OPENSSL-DTLS-CLIENT:<host>:<port>`

```
OPENSSL-DTLS-CLIENT:<host>:<port>
```

尝试建立到 `<host>` [IP 地址] 上 `<port>` [UDP 服务] 的 DTLS 连接，根据地址规范、名称解析或选项 `pf` 使用 UDP/IP 版本 4 或 6。  
`socat` 根据 `openssl-commonname` 选项或主机名检查对等证书的 subjectAltName 或 commonName。支持证书中的通配符。  
使用 `socat` 选项 `-b` 使数据报足够小，以便连同开销适合网络。使用选项 `-T` 防止对等方静默关闭时无限挂起。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`OPENSSL`、`RETRY`  
有用选项：`min-proto-version`、`cipher`、`verify`、`commonname`、`cafile`、`capath`、`certificate`、`key`、`compress`、`bind`、`pf`、`sourceport`、`retry`、`rcvtimeo`  
另请参阅：`OPENSSL-DTLS-SERVER`、`OPENSSL-CONNECT`、`UDP-CONNECT`

### `OPENSSL-DTLS-SERVER:<port>`

```
OPENSSL-DTLS-SERVER:<port>
```

在 UDP `<port>` [UDP 服务] 上监听。IP 版本为 4，或由 `pf` 指定。当连接被接受时，此地址表现为 DTLS 服务器。  
注意：你可能希望对此地址使用 `certificate` 选项。  
注意：客户端证书仅根据 `cafile` 或 `capath` 检查有效性，而不检查与客户端名称或其 IP 地址的匹配！使用 `socat` 选项 `-b` 使数据报足够小，以便连同开销适合网络。使用选项 `-T` 防止对等方静默关闭时无限挂起。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`LISTEN`、`OPENSSL`、`CHILD`、`RANGE`、`RETRY`  
有用选项：`pf`、`min-proto-version`、`cipher`、`verify`、`commonname`、`cafile`、`capath`、`certificate`、`key`、`compress`、`fork`、`bind`、`range`、`tcpwrap`、`su`、`reuseaddr`、`retry`、`rcvtimeo`  
另请参阅：`OPENSSL-DTLS-CLIENT`、`OPENSSL-LISTEN`、`UDP-LISTEN`

### `PIPE:<filename>`

```
PIPE:<filename>
```

如果 `<filename>` 已存在，则打开它。如果它不存在，则创建并打开一个命名管道。从 `socat` 1.4.3 版本开始，当地址关闭时删除命名管道（但请参见选项 `unlink-close`）。  
注意：当管道同时用于读取和写入时，它作为回显服务工作。  
注意：当管道同时用于读取和写入，并且 `socat` 尝试写入的字节数超过管道可缓冲的字节数（Linux 2.4：`2048` 字节）时，`socat` 可能会阻塞。考虑使用 `socat` 选项，例如 `-b 2048`。  
选项组：`FD`、`NAMED`、`OPEN`  
有用选项：`rdonly`、`nonblock`、`group`、`user`、`mode`、`unlink-early`  
另请参阅：无名管道

### `PIPE`

创建无名管道并将其用于读取和写入。它作为回显工作，因为写入它的所有内容都会立即作为读取数据出现。  
注意：当 `socat` 尝试写入的字节数超过管道可排队的字节数（Linux 2.4：`2048` 字节）时，`socat` 可能会阻塞。考虑例如使用选项 `-b 2048`。  
选项组：`FD`  
另请参阅：命名管道、`SOCKETPAIR`

### `SOCKETPAIR`

创建 `socketpair` 并将其用于读取和写入。它作为回显工作，因为写入它的所有内容都会立即作为读取数据出现。默认套接字类型是数据报，因此它保留数据包边界。  
选项组：`FD`  
有用选项：`socktype`  
另请参阅：无名管道

### `STALL`

此地址的读取部分从不提供任何数据，也不提供 `EOF`；写入部分从不准备好写入数据。这可能对测试和某些特殊场景有用。

### `TEXT:<string>`

```
TEXT:<string>
```

作为参数提供的文本被当作输入数据：它被缓冲在内部管道中，然后照常处理。标准转换会应用于该字符串，因此你可以检查参数如何被解析和准备，这对于像 `EXEC` 这样的地址很关键。  
此地址上的输出发送到 `stdout`。因此此地址可以替换如下构造：

```sh
echo "<string>" | socat STDIO TCP:<server>:<port>
```

替换为：

```sh
socat TEXT:"<string>\n" TCP:<server>:<port>
```

请查看下面带有 `sudo` 的示例。

### `POSIXMQ-READ:/<mqueue>`

```
POSIXMQ-READ:/<mqueue>
```

打开或创建指定的 POSIX 消息队列并读取消息（数据包）。它保留数据包边界。这是只读地址，请参见选项 `-u` 和 `-U` 以及双地址。  
`socat` 仅在 Linux 上提供此地址类型，因为那里的 POSIX MQ 基于 UNIX 文件描述符。  
有用选项：`posixmq-priority`、`unlink-early`、`unlink-close`、`o-nonblock`、`o-creat`、`o-excl`、`umask`

### `POSIXMQ-RECEIVE:/<mqueue>`, `POSIXMQ-RECV:/<mqueue>`

```
POSIXMQ-RECEIVE:/<mqueue>
POSIXMQ-RECV:/<mqueue>
```

打开或创建指定的 POSIX 消息队列并读取一条消息（数据包）。  
这是只读地址。更多信息请参见 `POSIXMQ-READ`。  
示例：带 `fork` 的 POSIX MQ 接收  
有用选项：`posixmq-priority`、`fork`、`max-children`、`unlink-early`、`unlink-close`、`o-creat`、`o-excl`、`umask`

### `POSIXMQ-SEND:/<mqueue>`

```
POSIXMQ-SEND:/<mqueue>
```

打开或创建指定的 POSIX 消息队列并写入消息（数据包）。  
这是只写地址。更多信息请参见 `POSIXMQ-READ`。  
（示例）  
有用选项：`posixmq-priority`、`posixmq-flush`、`fork`、`max-children`、`unlink-early`、`unlink-close`、`o-creat`、`o-excl`、`umask`

### `POSIXMQ-WRITE:/<mqueue>`

```
POSIXMQ-WRITE:/<mqueue>
```

与 `POSIXMQ-SEND` 相同。

### `POSIXMQ-BIDIRECTIONAL:/mqueue`, `POSIXMQ:/mqueue`

```
POSIXMQ-BIDIRECTIONAL:/mqueue
POSIXMQ:/mqueue
```

根据上下文以读取和/或写入模式打开或创建指定的 POSIX 消息队列，然后读取和/或写入消息（数据包）。在双向模式下，这只是另一个回显服务。`POSIXMQ` 拒绝双向模式以防止队列意外刷新；需要时使用 `POSIXMQ-BIDIRECTIONAL`。  
更多信息请参见 `POSIXMQ-READ` 和 `POSIXMQ-SEND`。

### `PROXY:<proxy>:<hostname>:<port>`

```
PROXY:<proxy>:<hostname>:<port>
```

连接到端口 `8080` 上的 HTTP 代理服务器，根据地址规范、名称解析或选项 `pf` 使用 TCP/IP 版本 4 或 6，并为 `hostname:port` 发送 `CONNECT` 请求。如果代理授予访问权限并成功连接到目标，`socat` 与目标之间的数据传输就可以开始（示例）。注意，流量不必是 HTTP，可以是任意协议。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`HTTP`、`RETRY`  
有用选项：`proxyport`、`ignorecr`、`proxyauth`、`resolve`、`crnl`、`bind`、`connect-timeout`、`mss`、`sourceport`、`retry`  
另请参阅：`SOCKS`、`TCP`

### `PTY`

生成伪终端（pty）并使用其主端。另一个进程可以像串行线或终端一样打开该 pty 的从端（示例）。如果 `ptmx` 和 `openpty` 机制都可用，则使用 `ptmx`（POSIX）。  
选项组：`FD`、`NAMED`、`PTY`、`TERMIOS`  
有用选项：`link`、`openpty`、`wait-slave`、`mode`、`user`、`group`  
另请参阅：`UNIX-LISTEN`、`PIPE`、`EXEC`、`SYSTEM`、`SHELL`

### `READLINE`

在 `stdio` 上使用 GNU readline 和历史记录，以允许编辑和重用输入行（示例）。这需要 GNU readline 和历史记录库。注意 `stdio` 应该是（伪）终端设备，否则 readline 似乎无法工作。  
选项组：`FD`、`READLINE`、`TERMIOS`  
有用选项：`history`、`noecho`  
另请参阅：`STDIO`

### `SCTP-CONNECT:<host>:<port>`

```
SCTP-CONNECT:<host>:<port>
```

建立到指定 `<host>` [IP 地址] 和 `<port>` [TCP 服务] 的 SCTP 流连接，根据地址规范、名称解析或选项 `pf` 使用 IP 版本 4 或 6。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`SCTP`、`CHILD`、`RETRY`  
有用选项：`bind`、`pf`、`connect-timeout`、`tos`、`mtudiscover`、`mtudiscover6`、`sctp-maxseg`、`sctp-nodelay`、`nonblock`、`sourceport`、`retry`、`readbytes`  
另请参阅：`SCTP4-CONNECT`、`SCTP6-CONNECT`、`SCTP-LISTEN`、`TCP-CONNECT`

### `SCTP4-CONNECT:<host>:<port>`

```
SCTP4-CONNECT:<host>:<port>
```

类似 `SCTP-CONNECT`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`、`SCTP`、`CHILD`、`RETRY`

### `SCTP6-CONNECT:<host>:<port>`

```
SCTP6-CONNECT:<host>:<port>
```

类似 `SCTP-CONNECT`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`SCTP`、`CHILD`、`RETRY`

### `SCTP-LISTEN:<port>`

```
SCTP-LISTEN:<port>
```

在 `<port>` [TCP 服务] 上监听并接受 SCTP 连接。IP 版本为 4，或由地址选项 `pf`、`socat` 选项（`-4`、`-6`）或环境变量 `SOCAT_DEFAULT_LISTEN_IP` 指定。注意，打开此地址通常会阻塞直到客户端连接。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`IP6`、`SCTP`、`RETRY`  
有用选项：`crnl`、`fork`、`bind`、`range`、`tcpwrap`、`pf`、`max-children`、`backlog`、`accept-timeout`、`sctp-maxseg`、`sctp-nodelay`、`su`、`reuseaddr`、`retry`  
另请参阅：`SCTP4-LISTEN`、`SCTP6-LISTEN`、`TCP-LISTEN`、`SCTP-CONNECT`

### `SCTP4-LISTEN:<port>`

```
SCTP4-LISTEN:<port>
```

类似 `SCTP-LISTEN`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`SCTP`、`RETRY`

### `SCTP6-LISTEN:<port>`

```
SCTP6-LISTEN:<port>
```

类似 `SCTP-LISTEN`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP6`、`SCTP`、`RETRY`

### `SOCKET-CONNECT:<domain>:<protocol>:<remote-address>`

```
SOCKET-CONNECT:<domain>:<protocol>:<remote-address>
```

使用前两个给定套接字参数和 `SOCK_STREAM` 创建流套接字（参见 `man socket(2)`），并连接到 `remote-address`。这两个套接字参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`remote-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
请注意，除了指定组的选项之外，当应用 `socat` 选项 `-g` 时，还可以使用更高层协议的选项。  
选项组：`FD`、`SOCKET`、`CHILD`、`RETRY`  
有用选项：`bind`、`setsockopt`  
另请参阅：`TCP`、`UDP-CONNECT`、`UNIX-CONNECT`、`SOCKET-LISTEN`、`SOCKET-SENDTO`

### `SOCKET-DATAGRAM:<domain>:<type>:<protocol>:<remote-address>`

```
SOCKET-DATAGRAM:<domain>:<type>:<protocol>:<remote-address>
```

使用前三个给定套接字参数创建数据报套接字（参见 `man socket(2)`），并将传出数据发送到 `remote-address`。这三个套接字参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`remote-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
请注意，除了指定组的选项之外，当应用 `socat` 选项 `-g` 时，还可以使用更高层协议的选项。  
选项组：`FD`、`SOCKET`、`RANGE`  
有用选项：`bind`、`range`、`setsockopt`  
另请参阅：`UDP-DATAGRAM`、`IP-DATAGRAM`、`SOCKET-SENDTO`、`SOCKET-RECV`、`SOCKET-RECVFROM`

### `SOCKET-LISTEN:<domain>:<protocol>:<local-address>`

```
SOCKET-LISTEN:<domain>:<protocol>:<local-address>
```

使用前两个给定套接字参数和 `SOCK_STREAM` 创建流套接字（参见 `man socket(2)`），并在 `local-address` 上等待传入连接。这两个套接字参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`local-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
请注意，除了指定组的选项之外，当应用 `socat` 选项 `-g` 时，还可以使用更高层协议的选项。  
选项组：`FD`、`SOCKET`、`LISTEN`、`RANGE`、`CHILD`、`RETRY`  
有用选项：`setsockopt`、`setsockopt-listen`  
另请参阅：`TCP`、`UDP-CONNECT`、`UNIX-CONNECT`、`SOCKET-LISTEN`、`SOCKET-SENDTO`、`SOCKET-SENDTO`

### `SOCKET-RECV:<domain>:<type>:<protocol>:<local-address>`

```
SOCKET-RECV:<domain>:<type>:<protocol>:<local-address>
```

使用三个给定套接字参数创建套接字（参见 `man socket(2)`），并将其绑定到 `<local-address>`。接收到达的数据。这三个参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`local-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
选项组：`FD`、`SOCKET`、`RANGE`  
有用选项：`range`、`setsockopt`、`setsockopt-listen`  
另请参阅：`UDP-RECV`、`IP-RECV`、`UNIX-RECV`、`SOCKET-DATAGRAM`、`SOCKET-SENDTO`、`SOCKET-RECVFROM`

### `SOCKET-RECVFROM:<domain>:<type>:<protocol>:<local-address>`

```
SOCKET-RECVFROM:<domain>:<type>:<protocol>:<local-address>
```

使用三个给定套接字参数创建套接字（参见 `man socket(2)`），并将其绑定到 `<local-address>`。接收到达的数据并将回复发送回发送方。前三个参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`local-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
请参阅关于 `RECVFROM` 地址的说明。  
选项组：`FD`、`SOCKET`、`CHILD`、`RANGE`  
有用选项：`fork`、`range`、`setsockopt`、`setsockopt-listen`  
另请参阅：`UDP-RECVFROM`、`IP-RECVFROM`、`UNIX-RECVFROM`、`SOCKET-DATAGRAM`、`SOCKET-SENDTO`、`SOCKET-RECV`

### `SOCKET-SENDTO:<domain>:<type>:<protocol>:<remote-address>`

```
SOCKET-SENDTO:<domain>:<type>:<protocol>:<remote-address>
```

使用三个给定套接字参数创建套接字（参见 `man socket(2)`）。将传出数据发送到给定地址并接收回复。这三个参数必须用整数指定。请查阅操作系统文档和包含文件以找到适当的值。`remote-address` 必须是 `sockaddr` 结构的数据表示，不包含 `sa_family` 和（BSD）`sa_len` 组件。  
选项组：`FD`、`SOCKET`  
有用选项：`bind`、`setsockopt`、`setsockopt-listen`  
另请参阅：`UDP-SENDTO`、`IP-SENDTO`、`UNIX-SENDTO`、`SOCKET-DATAGRAM`、`SOCKET-RECV`、`SOCKET-RECVFROM`

### `ACCEPT-FD:<fdnum>`

```
ACCEPT-FD:<fdnum>
```

期望 `<fdnum>` 中有一个监听套接字，并接受一个或多个（使用 `fork` 选项时）连接。此地址类型在 `systemd` 控制的“inetd 模式”下有用。  
示例：（示例）  
选项组：`FD`、`SOCKET`、`TCP`、`CHILD`、`RETRY`  
有用选项：`fork`、`range`、`sourceport`、`lowport`、`tcpwrap`

### `SOCKS4:<socks-server>:<host>:<port>`

```
SOCKS4:<socks-server>:<host>:<port>
```

通过 `<socks-server>` [IP 地址] 连接到 `<host>` [IPv4 地址] 上的 `<port>` [TCP 服务]，根据地址规范、名称解析或选项 `pf` 使用 IP 版本 4 或 6 上的 SOCKS 版本 4 协议（示例）。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`SOCKS4`、`RETRY`  
有用选项：`socksuser`、`socksport`、`sourceport`、`pf`、`retry`  
另请参阅：`SOCKS5`、`SOCKS4A`、`PROXY`、`TCP`

### `SOCKS4A:<socks-server>:<host>:<port>`

```
SOCKS4A:<socks-server>:<host>:<port>
```

类似 `SOCKS4`，但使用 SOCKS 协议版本 4a，因此将主机名解析留给 SOCKS 服务器。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`SOCKS4`、`RETRY`

### `SOCKS5-CONNECT:<socks-server>:<socks-port>:<target-host>:<target-port>`

```
SOCKS5-CONNECT:<socks-server>:<socks-port>:<target-host>:<target-port>
```

### `SOCKS5-CONNECT:<socks-server>:<target-host>:<target-port>`

```
SOCKS5-CONNECT:<socks-server>:<target-host>:<target-port>
```

通过 `<socks-server>` [IP 地址] 连接到 `<target-host>` [IPv4 地址] 上的 `<target-port>` [TCP 服务]，使用 TCP 上的 SOCKS 版本 5 协议。目前不提供身份验证机制。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`CHILD`、`RETRY`  
有用选项：`socksport`、`socksuser`、`sockspass`、`sourceport`、`pf`、`retry`  
另请参阅：`SOCKS5-LISTEN`、`SOCKS4`、`SOCKS4A`、`PROXY`、`TCP`

### `SOCKS5-LISTEN:<socks-server>:<socks-port>:<listen-host>:<listen-port>`

```
SOCKS5-LISTEN:<socks-server>:<socks-port>:<listen-host>:<listen-port>
```

### `SOCKS5-LISTEN:<socks-server>:<listen-host>:<listen-port>`

```
SOCKS5-LISTEN:<socks-server>:<listen-host>:<listen-port>
```

使用 TCP 上的 SOCKS 版本 5 协议连接到 `<socks-server>` [IP 地址]，并使其在 `<listen-port>` [TCP 服务] 上监听传入连接，绑定到 `<listen-host>` [IPv4 地址]。目前不提供身份验证机制。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`CHILD`、`RETRY`  
有用选项：`sourceport`、`pf`、`retry`  
另请参阅：`SOCKS5-CONNECT`

### `STDERR`

使用文件描述符 `2`。  
这是只写地址，请参见选项 `-u` 和 `-U`，以及双地址。  
选项组：`FD`（`TERMIOS`、`REG`、`SOCKET`）  
另请参阅：`FD`

### `STDIN`

使用文件描述符 `0`。  
这是只读地址，请参见选项 `-u` 和 `-U`，以及双地址。  
选项组：`FD`（`TERMIOS`、`REG`、`SOCKET`）  
有用选项：`readbytes`  
另请参阅：`FD`

### `STDIO`

使用文件描述符 `0` 进行读取，使用 `1` 进行写入。  
选项组：`FD`（`TERMIOS`、`REG`、`SOCKET`）  
有用选项：`readbytes`  
另请参阅：`FD`

### `STDOUT`

使用文件描述符 `1`。  
这是只写地址，请参见选项 `-u` 和 `-U`，以及双地址。  
选项组：`FD`（`TERMIOS`、`REG`、`SOCKET`）  
另请参阅：`FD`

### `SHELL:<shell-command>`, `SHELL`

```
SHELL:<shell-command>
SHELL
```

派生一个子进程，使其与父进程建立通信，并使用配置的 shell（`$SHELL`）调用指定程序。注意 `<shell-command>` [字符串] 不得包含 `,` 或 `!!`，并且 `:` 和 shell 元字符可能需要保护。程序成功启动后，`socat` 将数据写入进程的 `stdin`，并从其 `stdout` 读取。  
不带参数调用时，这会打开交互式 shell。  
选项组：`FD`、`SOCKET`、`EXEC`、`FORK`、`TERMIOS`  
有用选项：`path`、`fdin`、`fdout`、`chroot`、`su`、`su-d`、`nofork`、`socktype`、`pty`、`stderr`、`ctty`、`setsid`、`pipes`、`umask`、`sigint`、`sigquit`  
另请参阅：`EXEC`、`SYSTEM`

### `SYSTEM:<shell-command>`

```
SYSTEM:<shell-command>
```

派生一个子进程，使其与父进程建立通信，并使用 `system()` 调用指定程序。请注意 `<shell-command>` [字符串] 不得包含 `,` 或 `!!`，并且 shell 元字符可能需要保护。程序成功启动后，`socat` 将数据写入进程的 `stdin`，并从其 `stdout` 读取。  
选项组：`FD`、`SOCKET`、`EXEC`、`FORK`、`TERMIOS`  
有用选项：`path`、`fdin`、`fdout`、`chroot`、`su`、`su-d`、`nofork`、`socktype`、`pty`、`stderr`、`ctty`、`setsid`、`pipes`、`umask`、`sigint`、`sigquit`、`netns`  
另请参阅：`EXEC`、`SHELL`

### `TCP:<host>:<port>`

```
TCP:<host>:<port>
```

连接到 `<host>` [IP 地址] 上的 `<port>` [TCP 服务]，根据地址规范、名称解析或选项 `pf` 使用 TCP/IP 版本 4 或 6。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`TCP`、`RETRY`  
有用选项：`connect-timeout`、`retry`、`sourceport`、`netns`、`crnl`、`bind`、`pf`、`tos`、`mtudiscover`、`mtudiscover6`、`mss`、`nodelay`、`nonblock`、`readbytes`  
另请参阅：`TCP4`、`TCP6`、`TCP-LISTEN`、`UDP`、`SCTP-CONNECT`、`UNIX-CONNECT`

### `TCP4:<host>:<port>`

```
TCP4:<host>:<port>
```

类似 `TCP`，但仅支持 IPv4 协议（示例）。  
选项组：`FD`、`SOCKET`、`IP4`、`TCP`、`RETRY`

### `TCP6:<host>:<port>`

```
TCP6:<host>:<port>
```

类似 `TCP`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`TCP`、`RETRY`

### `TCP-LISTEN:<port>`

```
TCP-LISTEN:<port>
```

在 `<port>` [TCP 服务] 上监听并接受 TCP/IP 连接。IP 版本为 4，或由地址选项 `pf`、`socat` 选项（`-4`、`-6`）或环境变量 `SOCAT_DEFAULT_LISTEN_IP` 指定。注意，打开此地址通常会阻塞直到客户端连接。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`IP6`、`TCP`、`RETRY`  
有用选项：`crnl`、`fork`、`bind`、`range`、`tcpwrap`、`pf`、`max-children`、`backlog`、`accept-timeout`、`mss`、`su`、`reuseaddr`、`retry`、`cool-write`  
另请参阅：`TCP4-LISTEN`、`TCP6-LISTEN`、`UDP-LISTEN`、`SCTP-LISTEN`、`UNIX-LISTEN`、`OPENSSL-LISTEN`、`TCP-CONNECT`

### `TCP4-LISTEN:<port>`

```
TCP4-LISTEN:<port>
```

类似 `TCP-LISTEN`，但仅支持 IPv4 协议（示例）。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`TCP`、`RETRY`

### `TCP6-LISTEN:<port>`

```
TCP6-LISTEN:<port>
```

类似 `TCP-LISTEN`，但仅支持 IPv6 协议。  
额外有用选项：`ipv6only`  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP6`、`TCP`、`RETRY`

### `TUN[:<if-addr>/<bits>]`

```
TUN[:<if-addr>/<bits>]
```

创建 Linux TUN/TAP 设备，并可选地为其分配参数给出的地址和网络掩码。生成的网络接口几乎已可供其他进程使用；`socat` 服务其“线路侧”。此地址需要对隧道克隆设备（通常是 `/dev/net/tun`）的读写访问权限，以及执行某些 `ioctl()` 的权限。

> 需要选项 `iff-up` 才能立即激活接口！

注意：如果你打算在两个 `socat`“线路侧”之间传输数据包，你需要一种保留数据包边界的协议，例如 `UDP`；`TCP` 在配合选项 `nodelay` 时可能可行。  
选项组：`FD`、`NAMED`、`OPEN`、`TUN`  
有用选项：`iff-up`、`tun-device`、`tun-name`、`tun-type`、`interface-mtu`、`iff-no-pi`、`netns`  
另请参阅：`ip-recv`

### `UDP:<host>:<port>`

```
UDP:<host>:<port>
```

连接到 `<host>` [IP 地址] 上的 `<port>` [UDP 服务]，根据地址规范、名称解析或选项 `pf` 使用 UDP/IP 版本 4 或 6。  
请注意，由于 UDP 协议属性，不会建立真正的连接；必须发送数据才能“连接”到服务器，并且无法传输文件结束条件。  
从 1.8.1.0 版本开始，关闭时套接字会发送一个零长度 UDP 数据包，这可能触发对等方的 `EOF`（隐式选项 `shut-null`）。使用选项 `shut-none` 恢复旧行为。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`  
有用选项：`ttl`、`tos`、`bind`、`sourceport`、`pf`  
另请参阅：`UDP4`、`UDP6`、`UDP-LISTEN`、`TCP`、`IP`

### `UDP4:<host>:<port>`

```
UDP4:<host>:<port>
```

类似 `UDP`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`

### `UDP6:<host>:<port>`

```
UDP6:<host>:<port>
```

类似 `UDP`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`

### `UDP-DATAGRAM:<address>:<port>`

```
UDP-DATAGRAM:<address>:<port>
```

将传出数据发送到指定地址，该地址尤其可以是广播或多播地址。仅在使用了选项 `sourceport` 时，才会检查到达本地套接字的数据包是否具有正确的远程端口（这是 `Socat` 1.7.4.0 版本的变化），并且检查其源地址是否匹配 `RANGE` 或 `TCPWRAP` 选项。此地址类型例如可用于实现对称或非对称广播或多播通信。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`RANGE`  
有用选项：`bind`、`range`、`tcpwrap`、`broadcast`、`ip-multicast-loop`、`ip-multicast-ttl`、`ip-multicast-if`、`ip-add-membership`、`ip-add-source-membership`、`ipv6-join-group`、`ipv6-join-source-group`、`ttl`、`tos`、`sourceport`、`pf`  
另请参阅：`UDP4-DATAGRAM`、`UDP6-DATAGRAM`、`UDP-SENDTO`、`UDP-RECVFROM`、`UDP-RECV`、`UDP-CONNECT`、`UDP-LISTEN`、`IP-DATAGRAM`

### `UDP4-DATAGRAM:<address>:<port>`

```
UDP4-DATAGRAM:<address>:<port>
```

类似 `UDP-DATAGRAM`，但仅支持 IPv4 协议（示例 1、示例 2）。  
选项组：`FD`、`SOCKET`、`IP4`、`RANGE`

### `UDP6-DATAGRAM:<address>:<port>`

```
UDP6-DATAGRAM:<address>:<port>
```

类似 `UDP-DATAGRAM`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`RANGE`

### `UDP-LISTEN:<port>`

```
UDP-LISTEN:<port>
```

等待到达 `<port>` [UDP 服务] 的 UDP/IP 数据包，并“连接”回发送方。接受的 IP 版本为 4，或由选项 `pf` 指定。请注意，由于 UDP 协议属性，不会建立真正的连接；数据必须先来自对等方，因此打开此地址通常会阻塞直到客户端连接。此外，UDP 中未规定文件结束条件。  
从 1.8.1.0 版本开始，关闭时套接字会发送一个零长度 UDP 数据包，这可能触发对等方的 `EOF`（隐式选项 `shut-null`）。使用选项 `shut-none` 恢复旧行为。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`、`IP6`  
有用选项：`fork`、`bind`、`range`、`pf`  
另请参阅：`UDP`、`UDP4-LISTEN`、`UDP6-LISTEN`、`TCP-LISTEN`

### `UDP4-LISTEN:<port>`

```
UDP4-LISTEN:<port>
```

类似 `UDP-LISTEN`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP4`

### `UDP6-LISTEN:<port>`

```
UDP6-LISTEN:<port>
```

类似 `UDP-LISTEN`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RANGE`、`IP6`

### `UDP-SENDTO:<host>:<port>`

```
UDP-SENDTO:<host>:<port>
```

与指定对等套接字通信，该套接字由 `<host>` [IP 地址] 上的 `<port>` [UDP 服务] 定义，根据地址规范、名称解析或选项 `pf` 使用 UDP/IP 版本 4 或 6。它只向该对等套接字发送数据包并从中接收数据包。此地址有效地实现数据报客户端。它与 `socat` 的 `UDP-RECVFROM` 和 `UDP-RECV` 地址对等方配合良好。当对等方可能先发送数据时，`UDP-DATAGRAM` 更可取。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`  
有用选项：`ttl`、`tos`、`bind`、`sourceport`、`pf`  
另请参阅：`UDP4-SENDTO`、`UDP6-SENDTO`、`UDP-RECVFROM`、`UDP-RECV`、`UDP-CONNECT`、`UDP-LISTEN`、`IP-SENDTO`

### `UDP4-SENDTO:<host>:<port>`

```
UDP4-SENDTO:<host>:<port>
```

类似 `UDP-SENDTO`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`

### `UDP6-SENDTO:<host>:<port>`

```
UDP6-SENDTO:<host>:<port>
```

类似 `UDP-SENDTO`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`

### `UDP-RECVFROM:<port>`

```
UDP-RECVFROM:<port>
```

使用 UDP/IP 版本 4 或 6（取决于选项 `pf`）在 `<port>` [UDP 服务] 上创建 UDP 套接字。它从未指定的对等方接收一个数据包，并可以向该对等方发送一个或多个应答数据包。此模式在配合 `fork` 选项时特别有用，其中每个到达的数据包（来自任意对等方）由自己的子进程处理。这允许类似典型基于 UDP 的服务器（如 `ntpd` 或 `named`）的行为。此地址与 `socat` 的 `UDP-SENDTO` 地址对等方配合良好。  
注意：当第二个地址在进入传输循环之前失败时，数据包会被丢弃。在第二个地址上使用选项 `retry` 或 `forever` 以避免数据丢失。当你知道对等方地址时，`UDP-DATAGRAM` 更可取。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`CHILD`、`RANGE`  
有用选项：`fork`、`ttl`、`tos`、`bind`、`sourceport`、`pf`  
另请参阅：`UDP4-RECVFROM`、`UDP6-RECVFROM`、`UDP-SENDTO`、`UDP-RECV`、`UDP-CONNECT`、`UDP-LISTEN`、`IP-RECVFROM`、`UNIX-RECVFROM`

### `UDP4-RECVFROM:<port>`

```
UDP4-RECVFROM:<port>
```

类似 `UDP-RECVFROM`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`、`CHILD`、`RANGE`

### `UDP6-RECVFROM:<port>`

```
UDP6-RECVFROM:<port>
```

类似 `UDP-RECVFROM`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`CHILD`、`RANGE`

### `UDP-RECV:<port>`

```
UDP-RECV:<port>
```

使用 UDP/IP 版本 4 或 6（取决于选项 `pf`）在 `<port>` [UDP 服务] 上创建 UDP 套接字。它从多个未指定的对等方接收数据包并合并数据。不可能回复。它与例如 `socat` 的 `UDP-SENDTO` 地址对等方配合良好；其行为类似于 `syslog` 服务器。  
这是只读地址，请参见选项 `-u` 和 `-U`，以及双地址。  
注意：如果你需要 `fork` 选项，请改用单向模式（配合选项 `-u`）的 `UDP-RECVFROM`。  
选项组：`FD`、`SOCKET`、`IP4`、`IP6`、`RANGE`  
有用选项：`pf`、`bind`、`sourceport`、`ttl`、`tos`  
另请参阅：`UDP4-RECV`、`UDP6-RECV`、`UDP-SENDTO`、`UDP-RECVFROM`、`UDP-CONNECT`、`UDP-LISTEN`、`IP-RECV`、`UNIX-RECV`

### `UDP4-RECV:<port>`

```
UDP4-RECV:<port>
```

类似 `UDP-RECV`，但仅支持 IPv4 协议。  
选项组：`FD`、`SOCKET`、`IP4`、`RANGE`

### `UDP6-RECV:<port>`

```
UDP6-RECV:<port>
```

类似 `UDP-RECV`，但仅支持 IPv6 协议。  
选项组：`FD`、`SOCKET`、`IP6`、`RANGE`

### UDPLITE 系列地址

```
UDPLITE-CONNECT:<host>:<port>
UDPLITE4-CONNECT:<host>:<port>
UDPLITE6-CONNECT:<host>:<port>
UDPLITE-DATAGRAM:<address>:<port>
UDPLITE4-DATAGRAM:<address>:<port>
UDPLITE6-DATAGRAM:<address>:<port>
UDPLITE-LISTEN:<port>
UDPLITE4-LISTEN:<port>
UDPLITE6-LISTEN:<port>
UDPLITE-SENDTO:<host>:<port>
UDPLITE4-SENDTO:<host>:<port>
UDPLITE6-SENDTO:<host>:<port>
UDPLITE-RECVFROM:<port>
UDPLITE4-RECVFROM:<port>
UDPLITE6-RECVFROM:<port>
UDPLITE-RECV:<port>
UDPLITE4-RECV:<port>
UDPLITE6-RECV:<port>
```

`UDPLITE` 地址与相关 `UDP` 地址几乎相同，但它们使用 UDP-Lite 协议，并具有额外的 `UDPLITE` 选项组。

### `UNIX-CONNECT:<filename>`

```
UNIX-CONNECT:<filename>
```

连接到 `<filename>`，假定它是 UNIX 域套接字。如果 `<filename>` 不存在，这是错误；如果 `<filename>` 不是 UNIX 域套接字，这是错误；如果 `<filename>` 是 UNIX 域套接字但没有进程在监听，这是错误。  
选项组：`FD`、`SOCKET`、`NAMED`、`RETRY`、`UNIX`  
有用选项：`bind`  
另请参阅：`UNIX-LISTEN`、`UNIX-SENDTO`、`TCP`

### `UNIX-LISTEN:<filename>`

```
UNIX-LISTEN:<filename>
```

使用 UNIX 域流套接字在 `<filename>` 上监听并接受连接。如果 `<filename>` 存在且不是套接字，这是错误。如果 `<filename>` 存在且是 UNIX 域套接字，则绑定到该地址会失败（请使用选项 `unlink-early`！）。注意，打开此地址通常会阻塞直到客户端连接。从 `socat` 1.4.3 版本开始，当地址关闭时删除文件系统条目（但请参见选项 `unlink-close`）（示例）。  
选项组：`FD`、`SOCKET`、`NAMED`、`LISTEN`、`CHILD`、`RETRY`、`UNIX`  
有用选项：`fork`、`umask`、`mode`、`user`、`group`、`unlink-early`  
另请参阅：`UNIX-CONNECT`、`UNIX-RECVFROM`、`UNIX-RECV`、`TCP-LISTEN`

### `UNIX-SENDTO:<filename>`

```
UNIX-SENDTO:<filename>
```

与指定对等套接字通信，该套接字由 [ `<filename>` ] 定义，假定它是 UNIX 域数据报套接字。它只向该对等套接字发送数据包并从中接收数据包。请注意，可能有必要将本地套接字绑定到某个地址（例如 `/tmp/sock1`，该地址之前必须不存在）。此地址类型与 `socat` 的 `UNIX-RECVFROM` 和 `UNIX-RECV` 地址对等方配合良好。  
选项组：`FD`、`SOCKET`、`NAMED`、`UNIX`  
有用选项：`bind`  
另请参阅：`UNIX-RECVFROM`、`UNIX-RECV`、`UNIX-CONNECT`、`UDP-SENDTO`、`IP-SENDTO`

### `UNIX-RECVFROM:<filename>`

```
UNIX-RECVFROM:<filename>
```

创建 UNIX 域数据报套接字 [ `<filename>` ]。接收一个数据包，并可以向该对等方发送一个或多个应答数据包。此模式在配合 `fork` 选项时特别有用，其中每个到达的数据包（来自任意对等方）由自己的子进程处理。此地址与 `socat` 的 `UNIX-SENDTO` 地址对等方配合良好。  
选项组：`FD`、`SOCKET`、`NAMED`、`CHILD`、`UNIX`  
请参阅关于 `RECVFROM` 地址的说明。  
有用选项：`fork`、`umask`  
另请参阅：`UNIX-SENDTO`、`UNIX-RECV`、`UNIX-LISTEN`、`UDP-RECVFROM`、`IP-RECVFROM`

### `UNIX-RECV:<filename>`

```
UNIX-RECV:<filename>
```

创建 UNIX 域数据报套接字 [ `<filename>` ]。从多个未指定的对等方接收数据包并合并数据。不可能回复；这是只读地址，请参见选项 `-u` 和 `-U`，以及双地址。例如，它可以由 `socat` 的 `UNIX-SENDTO` 地址对等方寻址。其行为类似于 `syslog` 服务器。  
选项组：`FD`、`SOCKET`、`NAMED`、`UNIX`  
有用选项：`umask`  
另请参阅：`UNIX-SENDTO`、`UNIX-RECVFROM`、`UNIX-LISTEN`、`UDP-RECV`、`IP-RECV`

### `UNIX-CLIENT:<filename>`

```
UNIX-CLIENT:<filename>
```

与指定对等套接字通信，该套接字由 [ `<filename>` ] 定义，假定它是 UNIX 域套接字。它首先尝试连接；如果失败，则假定它是数据报套接字，从而支持两种类型。  
选项组：`FD`、`SOCKET`、`NAMED`、`UNIX`  
有用选项：`bind`  
另请参阅：`UNIX-CONNECT`、`UNIX-SENDTO`、`GOPEN`

### `VSOCK-CONNECT:<cid>:<port>`

```
VSOCK-CONNECT:<cid>:<port>
```

建立到指定 `<cid>` [VSOCK cid] 和 `<port>` [VSOCK 端口] 的 VSOCK 流连接。  
选项组：`FD`、`SOCKET`、`CHILD`、`RETRY`  
有用选项：`bind`、`connect-timeout`、`retry`、`readbytes`  
另请参阅：`VSOCK-LISTEN`

### `VSOCK-LISTEN:<port>`

```
VSOCK-LISTEN:<port>
```

在 `<port>` [VSOCK 端口] 上监听并接受 VSOCK 连接。注意，打开此地址通常会阻塞直到客户端连接。  
选项组：`FD`、`SOCKET`、`LISTEN`、`CHILD`、`RETRY`  
有用选项：`fork`、`bind`、`max-children`、`backlog`、`su`、`reuseaddr`、`retry`  
另请参阅：`VSOCK-CONNECT`

### `ABSTRACT-CONNECT:<string>`, `ABSTRACT-LISTEN:<string>`, `ABSTRACT-SENDTO:<string>`, `ABSTRACT-RECVFROM:<string>`, `ABSTRACT-RECV:<string>`, `ABSTRACT-CLIENT:<string>`

```
ABSTRACT-CONNECT:<string>
ABSTRACT-LISTEN:<string>
ABSTRACT-SENDTO:<string>
ABSTRACT-RECVFROM:<string>
ABSTRACT-RECV:<string>
ABSTRACT-CLIENT:<string>
```

`ABSTRACT` 地址与相关 `UNIX` 地址几乎相同，区别在于它们不寻址基于文件系统的套接字，而是寻址备用 UNIX 域地址空间。为实现这一点，套接字地址字符串在内部以 `"\0"` 为前缀。此特性可用（仅？）于 Linux。选项组与相关 `UNIX` 地址相同，除了 `ABSTRACT` 地址不是 `NAMED` 组的成员。  
有用选项：`netns`

## 示例

```sh
socat - TCP4:www.domain.org:80
```

在 `STDIO`（`-`）与到主机 `www.domain.org` 端口 `80` 的 `TCP4` 连接之间传输数据。此示例产生类似 `telnet` 或 `netcat` 的交互式连接。`stdin` 终端参数不会改变，因此你可以用 `^D` 关闭中继，或用 `^C` 中止它。

```sh
socat -d -d \
READLINE,history=$HOME/.http_history \
TCP4:www.domain.org:www,crnl
```

这类似上一示例，但你可以以类似 bash 的方式编辑当前行（`READLINE`），并使用历史文件 `.http_history`；`socat` 打印进度消息（`-d -d`）。端口由服务名（`www`）指定，并使用正确的网络行终止字符（`crnl`）而不是 `NL`。

```sh
socat \
TCP4-LISTEN:www \
TCP4:www.domain.org:www
```

安装一个简单的 TCP 端口转发器。使用 `TCP4-LISTEN`，它在本地端口 “www” 上监听，直到有连接到来，接受该连接，然后连接到远程主机（`TCP4`）并开始数据传输。它不会接受第二个连接。

```sh
socat -d -d -lmlocal2 \
TCP4-LISTEN:80,bind=myaddr1,reuseaddr,fork,su=nobody,range=10.0.0.0/8 \
TCP4:www.domain.org:80,bind=myaddr2
```

TCP 端口转发器，每一侧绑定到另一个本地 IP 地址（`bind`）。此示例通过在每个 `accept()` 之后 `fork` 新进程来处理几乎任意数量的并行或连续连接。它通过在 `fork` 后 `su` 到用户 `nobody` 提供一点安全性；它只允许来自私有 `10` 网络（`range`）的连接；由于 `reuseaddr`，它允许在主进程终止后立即重启，即使某些子套接字尚未完全关闭。使用 `-lmlocal2`，`socat` 记录到 `stderr`，直到成功到达接受循环。进一步日志记录定向到 `syslog`，设施为 `local2`。

```sh
socat \
TCP4-LISTEN:5555,fork,tcpwrap=script \
EXEC:/bin/myscript,chroot=/home/sandbox,su-d=sandbox,pty,stderr
```

一个简单的服务器，接受连接（`TCP4-LISTEN`）并为每个连接 `fork` 新子进程；每个子进程充当单个中继。客户端必须匹配 `/etc/hosts.allow` 和 `/etc/hosts.deny` 中守护进程名 “script” 的规则，否则会被拒绝访问（参见 “man 5 hosts_access”）。为了 `EXEC` 程序，子进程 `chroot` 到 `/home/sandbox`，`su` 到用户 `sandbox`，然后启动程序 `/home/sandbox/bin/myscript`。`Socat` 和 `myscript` 通过伪 tty（`pty`）通信；`myscript` 的 `stderr` 重定向到 `stdout`，因此其错误消息通过 `socat` 传输到连接的客户端。

```sh
socat \
EXEC:"mail.sh target@domain.com",fdin=3,fdout=4 \
TCP4:mail.relay.org:25,crnl,bind=alias1.server.org,mss=512
```

`mail.sh` 是随 `socat` 分发的 shell 脚本，实现一个简单的 SMTP 客户端。它被编程为在其 FD `3`（输入）和 `4`（输出）上“说” SMTP。`fdin` 和 `fdout` 选项告诉 `socat` 使用这些 FD 与程序通信。因为 `mail.sh` 继承 `stdin` 和 `stdout`，而 `socat` 不使用它们，所以脚本可以从 `stdin` 读取邮件正文。`Socat` 使 `alias1` 成为你的本地源地址（`bind`），处理正确的网络行终止（`crnl`），并且每个数据包最多发送 `512` 个数据字节（`mss`）。

```sh
socat \
-,escape=0x0f \
/dev/ttyS0,rawer,crnl
```

通过串行线打开交互式连接，例如与调制解调器通话。`rawer` 将控制台和 `ttyS0` 的终端参数设置为实用值，`crnl` 转换为正确的换行字符。`escape` 允许使用字符 `control-O` 终止 `socat` 进程。考虑使用 `READLINE` 代替第一个地址。

```sh
socat \
UNIX-LISTEN:/tmp/.X11-unix/X1,fork \
SOCKS4:host.victim.org:127.0.0.1:6000,socksuser=nobody,sourceport=20
```

使用 `UNIX-LISTEN`，`socat` 打开一个监听 UNIX 域套接字 `/tmp/.X11-unix/X1`。此路径对应于你机器上的本地 XWindow 显示 `:1`，因此接受发往 `DISPLAY=:1` 的 XWindow 客户端连接。`Socat` 然后与 SOCKS4 服务器 `host.victim.org` 通信，该服务器可能由于其静态 IP 过滤器中的 FTP 相关弱点而允许基于源端口 `20` 的连接。`Socat` 假装由 `socksuser nobody` 调用，并请求连接到回环端口 `6000`（只有弱 `sockd` 配置会允许）。因此我们获得与受害者 XWindow 服务器的连接；如果它不需要 MIT cookies 或 Kerberos 身份验证，我们就可以开始工作。请注意一次只能有一个连接，因为 TCP 对于给定的一组地址和端口只能建立一个会话。

```sh
socat -u \
/tmp/readdata,seek-end=0,ignoreeof \
STDIO
```

这是单向数据传输（`-u`）的示例。`Socat` 从文件 `/tmp/readdata`（隐式地址 `GOPEN`）传输数据，从当前末尾开始（`seek-end=0` 让 `socat` 从当前文件末尾开始读取；使用 `seek=0` 或不使用 seek 选项来先读取现有数据），以类似 “tail -f” 的模式（`ignoreeof`）。这个“文件”也可能是监听的 UNIX 域套接字（此时不要使用 seek 选项）。

```sh
(sleep 5; echo PASSWORD; sleep 5; echo ls; sleep 1) | \
socat - \
EXEC:'ssh -l user server',pty,setsid,ctty
```

`EXEC` 一个到 `server` 的 ssh 会话。使用 `pty` 在 `socat` 和 ssh 之间通信，使其成为 ssh 的控制 tty（`ctty`），并让此 pty 成为新进程组的所有者（`setsid`），因此 ssh 接受来自 `socat` 的密码。

```sh
socat -u \
TCP4-LISTEN:3334,reuseaddr,fork \
OPEN:/tmp/in.log,creat,append
```

实现一个简单的基于网络的消息收集器。对于每个连接到端口 `3334` 的客户端，生成新子进程（选项 `fork`）。客户端发送的所有数据都追加到文件 `/tmp/in.log`。如果文件不存在，`socat` 创建它。选项 `reuseaddr` 允许立即重启服务器进程。

```sh
socat \
READLINE,noecho='[Pp]assword:' \
EXEC:'ftp ftp.server.com',pty,setsid,ctty
```

在 `EXEC` 的 ftp 客户端实用程序周围包装命令行历史记录（`READLINE`）。这允许编辑和重用 FTP 命令，以便相对舒适地浏览 ftp 目录层次结构。密码会被回显！需要 `pty` 才能让 ftp 发出提示。尽管如此，密码和 FTP 提示可能会出现一些混乱。

```sh
socat \
PTY,link=$HOME/dev/vmodem0,rawer,wait-slave \
EXEC:'"ssh modemserver.us.org socat - /dev/ttyS0,nonblock,rawer"'
```

在客户端生成伪终端设备（`PTY`），可通过符号链接 `$HOME/dev/vmodem0` 访问。期望串行线或调制解调器的应用程序可以配置为使用 `$HOME/dev/vmodem0`；其流量将通过 ssh 定向到调制解调器服务器，那里另一个 `socat` 实例将其链接到 `/dev/ttyS0`。

```sh
sudo socat --experimental \
TCP4-LISTEN:8000,reuseaddr,fork,netns=namespace1 \
TCP4-CONNECT:server2:8000
```

在给定网络命名空间中创建监听器，接受端口 `8000` 上的 TCP 连接并将它们转发到 `server2`。

```sh
sudo socat --experimental \
TUN:192.168.2.1/24,up \
TUN:192.168.2.2/24,up,netns=namespace2
```

创建两个虚拟网络接口，一个在默认命名空间，另一个在 `namespace2`，并在它们之间转发数据包，充当虚拟网络连接。

```sh
socat \
TCP4-LISTEN:2022,reuseaddr,fork \
PROXY:proxy.local:www.domain.org:22,proxyport=3128,proxyauth=username:s3cr3t
```

启动一个转发器，接受端口 `2022` 上的连接，并使用 `CONNECT` 方法将它们通过位于主机 `proxy.local`、监听端口 `3128`（`proxyport`）的代理守护进程定向，在那里以 “username” 和 “s3cr3t” 进行身份验证（`proxyauth`）。然后 `proxy.local` 应建立到主机 `www.domain.org` 端口 `22` 的连接。

```sh
socat - \
SSL:server:4443,cafile=./server.crt,cert=./client.pem
```

是一个 OpenSSL 客户端，尝试与 SSL 服务器建立安全连接。选项 `cafile` 指定包含信任证书的文件：我们仅当服务器出示这些证书之一并证明其拥有相关私钥时才信任服务器。否则连接终止。通过 `cert` 指定包含客户端证书及相关私钥的文件。当服务器希望客户端身份验证时需要；许多 Internet 服务器不需要。第一个地址（`-`）几乎可以替换为任何其他 `socat` 地址。

```sh
socat \
OPENSSL-LISTEN:4443,reuseaddr,pf=ip4,fork,cert=./server.pem,cafile=./client.crt \
PIPE
```

是一个 OpenSSL 服务器，接受 TCP 连接，出示文件 `server.pem` 中的证书，并强制客户端出示根据 `cafile.crt` 验证的证书。第二个地址（`PIPE`）几乎可以替换为任何其他 `socat` 地址。有关生成和分发 OpenSSL 密钥和证书的说明，请参见额外的 socat 文档 `socat-openssl.txt`。

```sh
echo |
socat -u - \
FILE:/tmp/bigfile,create,largefile,seek=100000000000
```

创建一个 100GB+1B 的稀疏文件；这需要支持此功能的文件系统类型（`ext2`、`ext3`、`ext4`、`reiserfs`、`xfs`；不是 `minix`、`vfat`）。写入 1 字节的操作可能需要很长时间（`reiserfs`：几分钟；`ext2`：“没有”时间），并且生成的文件仅其 inode 就可能消耗一些磁盘空间（`reiserfs`：2MB；`ext2`：16KB）。

```sh
socat \
TCP-L:7777,reuseaddr,fork \
SYSTEM:'filan -i 0 -s >&2',nofork
```

在端口 `7777` 上监听传入 TCP 连接。对于每个接受的连接，调用一个 shell。此 shell 的 `stdin` 和 `stdout` 直接连接到 TCP 套接字（`nofork`）。shell 启动 `filan` 并让其将套接字地址打印到 `stderr`（你的终端窗口）。

```sh
socat \
STDIO,cfmakeraw \
SHELL,pty,setsid,ctty,stderr
```

在当前终端中创建 shell，提供作业控制、历史记录等。

```sh
echo -e "\0\14\0\0\c" |
socat -u - \
FILE:/usr/bin/squid.exe,seek=0x00074420
```

充当原始二进制编辑器：它将 4 个字节 `000 014 000 000` 写入可执行文件 `/usr/bin/squid.exe` 的偏移 `0x00074420` 处（这是 2004 年使 Cygwin 中的 squid 可执行文件在 Windows 下运行的真实补丁）。

```sh
socat - \
TCP:www.blackhat.org:31337,readbytes=1000
```

连接到未知服务并防止被洪水淹没。

```sh
socat -U \
TCP:target:9999,end-close \
TCP-L:8888,reuseaddr,fork
```

将来自端口 `8888` 上不同 TCP 流的数据合并到一个流到 `target:9999`。`end-close` 选项防止由第二个地址 `fork` 出的子进程终止到 `9999` 的共享连接（`close(2)` 只是取消链接 inode，只要父进程存活它就会保持活动；`shutdown(2)` 会主动终止连接）。

```sh
socat \
TCP-LISTEN:10021,reuseaddr,socktype=6,protocol=33,fork PIPE
```

是一个简单的 DCCP 回显服务器。DCCP 现在直接在 `socat` 中提供，但此示例展示如何使用 `socat` 的 TCP 过程并将套接字类型更改为 `SOCK_DCCP=6`（在 Linux 上），将 IP 协议更改为 `IPPROTO_DCCP=33`。

```sh
socat - \
TCP:<server>:10021,reuseaddr,socktype=6,protocol=33,fork
```

是一个简单的 DCCP 客户端。DCCP 现在直接在 `socat` 中提供，但此示例展示如何使用 `socat` 的 TCP 过程，但将套接字类型更改为 `SOCK_DCCP=6`（在 Linux 上），将 IP 协议更改为 `IPPROTO_DCCP=33`。

```sh
socat - \
UDP4-DATAGRAM:192.168.1.0:123,sp=123,broadcast,range=192.168.1.0/24
```

向网络 `192.168.1.0/24` 发送广播并接收那里时间服务器的回复。忽略来自此网络外部主机的 NTP 数据包。

```sh
socat - \
SOCKET-DATAGRAM:2:2:17:x007bxc0a80100x0000000000000000,bind=x007bx00000000x0000000000000000,setsockopt-int=1:6:1,range=x0000xc0a80100x0000000000000000:x0000xffffff00x0000000000000000
```

在语义上等同于上一示例，但所有参数都以通用形式指定。`setsockopt-int` 的值 `6` 是 Linux 中 `SO_BROADCAST` 的值。

```sh
socat - \
IP4-DATAGRAM:255.255.255.255:44,broadcast,range=10.0.0.0/8
```

使用协议 `44` 向本地网络发送广播。仅接受来自私有地址范围的回复。

```sh
socat - \
UDP4-DATAGRAM:224.255.0.1:6666,bind=:6666,ip-add-membership=224.255.0.1:eth0
```

使用 UDP 将数据从 `stdin` 传输到指定多播地址。本地和远程端口都是 `6666`。告诉接口 `eth0` 也接受给定组的多播数据包。本地网络上的多个主机可以运行此命令，因此任何主机发送的所有数据都将被所有其他主机接收。注意有许多可能的失败原因，包括 IP 过滤器、路由问题、操作系统选择错误接口、网桥或配置不良的交换机。

```sh
socat \
UDP:host2:4443 \
TUN:192.168.255.1/24,up
```

与 `host2` 建立虚拟（但非私有！）网络的一侧，其中可能运行类似进程，使用 `UDP-L` 和 tun 地址 `192.168.255.2`。它们可以使用地址 `192.168.255.1` 和 `192.168.255.2` 相互到达。注意通过 TCP 或 SSL 等进行流式传输并不保证保留数据包边界，因此可能导致数据包丢失。

```sh
socat - \
VSOCK-CONNECT:2:1234
```

与主机建立 VSOCK 连接（主机始终可通过众所周知的 `CID=2` 到达），端口 `1234`。

```sh
socat - \
VSOCK-LISTEN:1234
```

在端口 `1234` 上监听 VSOCK 连接。

```sh
socat - \
VSOCK-CONNECT:31:4321,bind:5555
```

与 `CID=31` 的客户机在端口 `1234` 上建立 VSOCK 连接，将本地套接字绑定到端口 `5555`。

```sh
socat \
VSOCK-LISTEN:3333,reuseaddr,fork \
VSOCK-CONNECT:42,3333
```

启动转发器，接受端口 `3333` 上的 VSOCK 连接，并将它们定向到 `CID=42` 的客户机的同一端口。

```sh
socat \
VSOCK-LISTEN:22,reuseaddr,fork \
TCP:localhost:22
```

将来自端口 `22` 的 VSOCK 连接转发到本地 SSH 服务器。在 VM 中运行此命令允许你从主机使用 VSOCK 通过 SSH 连接，如下例所示。

```sh
socat \
TCP4-LISTEN:22222,reuseaddr,fork \
VSOCK-CONNECT:33:22
```

将来自端口 `22222` 的 TCP 连接转发到 `CID=33` 且监听 VSOCK 端口 `22` 的客户机。在主机中运行此命令，如果客户机运行上面的示例，则允许你通过运行 `ssh -p 22222 user@localhost` 使用 SSH 连接。

```sh
socat \
PTY,link=/var/run/ppp,rawer \
INTERFACE:hdlc0
```

绕过 pppd 需要串行设备，因此可能无法在由网络设备表示的同步线上工作的问题。`socat` 创建 `PTY` 以使 pppd 满意，绑定到网络接口 `hdlc0`，并可以在两个设备之间传输数据。然后在设备 `/var/run/ppp` 上使用 pppd。

```sh
socat -u \
STDIO \
POSIXMQ-SEND:/queue1,unlink-early,mq-prio=10
```

将从 `stdio` 读取的数据包（即交互运行时的输入行）写入 POSIX 消息队列，优先级为 `10`。

```sh
socat -u \
POSIXMQ-RECV:/queue1,fork,max-children=3 \
SYSTEM:"worker.sh"
```

从 POSIX 消息队列接收消息（数据包），并对于每条消息 `fork` 一个子进程来读取和处理该消息。同时最多允许 `3` 个子进程。

```sh
socat -T 1 -d -d \
TCP-L:10081,reuseaddr,fork,crlf \
SYSTEM:"echo -e \"\\\"HTTP/1.0 200 OK\\\nDocumentType: text/plain\\\n\\\ndate: \$\(date\)\\\nserver:\$SOCAT_SOCKADDR:\$SOCAT_SOCKPORT\\\nclient: \$SOCAT_PEERADDR:\$SOCAT_PEERPORT\\\n\\\"\"; cat; echo -e \"\\\"\\\n\\\"\""
```

创建一个非常原始的 HTTP 回显服务器：每个连接的 HTTP 客户端都会得到一个有效的 HTTP 回复，其中包含服务器主机所看到的客户端地址和端口信息、主机地址（在多宿主服务器上可能不同）以及原始客户端请求。

```sh
socat -d -d \
UDP4-RECVFROM:9999,so-broadcast,so-timestamp,ip-pktinfo,ip-recverr,ip-recvopts,ip-recvtos,ip-recvttl!!- \
SYSTEM:'export; sleep 1' |
grep SOCAT
```

等待端口 `9999` 上的传入 UDP 数据包，并打印 `socat` 提供的环境变量。在基于 BSD 的系统上，必须将 `ip-pktinfo` 替换为 `ip-recvdstaddr,ip-recvif`。特别值得关注的是 `SOCAT_IP_DSTADDR`：它包含数据包的目标地址，可能是单播、多播或广播地址。

```sh
echo -e "M-SEARCH * HTTP/1.1\nHOST: 239.255.255.250:1900\nMAN: \"ssdp:discover\"\nMX: 4\nST: \"ssdp:all\"\n" |
socat - \
UDP-DATAGRAM:239.255.255.250:1900,crlf
```

向本地网络发送 SSDP（简单服务发现协议）查询，并收集和输出收到的应答。

```sh
systemd-socket-activate -l 1077 --inetd socat ACCEPT:0,fork PIPE
```

`systemd-socket-activate` 是用于测试守护进程 systemd 套接字激活的程序。使用 `--inetd` 时，它等待指定端口上的连接。它不接受连接，而是将监听文件描述符作为 FD `0` 和 `1` 传递。`Socat` 接受等待的连接并开始数据传输。

```sh
sudo socat -u TEXT:"0 $((2**31-1))" /proc/sys/net/ipv4/ping_group_range
```

使用 `sudo` 通过 `socat` 的 `TEXT` 地址将文本写入 `/proc/sys/` 文件，而不是将其通过管道传给 `sudo` 下的 `tee`。

## 诊断

`Socat` 使用日志机制，可按严重性过滤消息。提供的严重性或多或少兼容适当的 `syslog` 优先级。使用一次到四次 `-d` 命令行选项，可以选择发出消息的最低优先级。每条消息包含一个指定消息严重性的单个大写字符（`F`、`E`、`W`、`N`、`I` 或 `D` 之一）。

- FATAL  
    需要无条件立即终止程序的条件。

- ERROR  
    阻止程序正常处理的条件。通常程序终止（参见选项 `-s`）。

- WARNING  
    某些功能未正确工作，或处于无法保证正确进一步处理但可能仍可行的状态。

- NOTICE  
    程序的有趣动作，例如用于以某种服务器模式监督 `socat`。

- INFO  
    描述程序做什么，以及可能为什么发生。允许监视文件描述符的生命周期。

- DEBUG  
    描述程序如何工作、所有系统或库调用及其结果。

日志消息可以写入 `stderr`、文件或 `syslog`。

退出时，如果 `socat` 因 `EOF` 或不活动超时而终止，则状态为 `0`；错误时为正数；致命错误时为负数。

## 文件

- `/usr/bin/socat`
- `/usr/bin/filan`
- `/usr/bin/procan`

## 信号

- `SIGUSR1`  
    导致记录当前传输统计信息。另请参见选项 `--statistics`。

## 环境变量

输入变量将环境信息传递给 `socat`，输出变量由 `socat` 设置，供执行的脚本和程序使用。

在以 “SOCAT” 开头的输出变量中，该前缀实际上会被可执行文件的大写名称或选项 `-lp` 的值替换。

- `SOCAT_DEFAULT_LISTEN_IP`（输入）  
    （值 `4` 或 `6`）设置用于 `listen`、`recv` 和 `recvfrom` 地址的 IP 版本，如果未给出 `pf`（协议族）选项。被 `socat` 选项 `-4` 或 `-6` 覆盖。

- `SOCAT_PREFERRED_RESOLVE_IP`（输入）  
    （值 `0`、`4` 或 `6`）设置当版本未由地址类型、选项 `pf`（协议族）或地址格式指定时，解析目标主机名所使用的 IP 版本。如果名称解析未返回匹配条目，则采用第一个结果（具有不同 IP 版本）。值为 `0` 时，`socat` 始终选择第一条记录及其 IP 版本。

- `SOCAT_MAIN_WAIT`（输入）  
    指定在 `main()` 开始时主进程睡眠的时间（秒）。用于调试。

- `SOCAT_TRANSFER_WAIT`（输入）  
    指定在打开地址之后、进入传输循环之前进程睡眠的时间（秒）。用于调试。

- `SOCAT_FORK_WAIT`（输入）  
    指定成功 `fork()` 后父进程和子进程睡眠的时间（秒）。用于调试。

- `SOCAT_VERSION`（输出）  
    `Socat` 将此变量设置为其版本字符串，例如发布版本为 “1.7.0.0”，临时版本例如 “1.6.0.1+envvar”；可在 `socat` 调用的脚本中使用。

- `SOCAT_PID`（输出）  
    `Socat` 将此变量设置为其进程 id。在 `fork` 地址选项情况下，`SOCAT_PID` 获得子进程 id。为 `exec`、`system` 和 `SHELL` 进行 `fork` 不会改变 `SOCAT_PID`。

- `SOCAT_PPID`（输出）  
    `Socat` 将此变量设置为其进程 id。在 `fork` 情况下，`SOCAT_PPID` 保留主进程的 pid。

- `SOCAT_PEERADDR`（输出）  
    对于被动套接字地址（所有 `LISTEN` 和 `RECVFROM` 地址），此变量设置为描述对等方套接字地址的字符串。不包含端口信息。

- `SOCAT_PEERPORT`（输出）  
    对于适当的被动套接字地址（`TCP`、`UDP` 和 `SCTP` 的 `LISTEN` 和 `RECVFROM`），此变量设置为包含对等方端口号的字符串。

- `SOCAT_SOCKADDR`（输出）  
    对于所有 `LISTEN` 地址，此变量设置为描述本地套接字地址的字符串。不包含端口信息（示例）。

- `SOCAT_SOCKPORT`（输出）  
    对于 `TCP-LISTEN`、`UDP-LISTEN` 和 `SCTP-LISTEN` 地址，此变量设置为本地端口。

- `SOCAT_TIMESTAMP`（输出）  
    对于应用了地址选项 `so-timestamp` 的所有 `RECVFROM` 地址，`socat` 将此变量设置为结果时间戳。

- `SOCAT_IP_OPTIONS`（输出）  
    对于应用了地址选项 `ip-recvopts` 的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 用接收数据包的 IP 选项填充此变量。

- `SOCAT_IP_DSTADDR`（输出）  
    对于应用了地址选项 `ip-recvdstaddr`（BSD）或 `ip-pktinfo`（其他平台）的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的目标地址。这对于识别广播和多播寻址的数据包特别有用。

- `SOCAT_IP_IF`（输出）  
    对于应用了地址选项 `ip-recvif`（BSD）或 `ip-pktinfo`（其他平台）的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的接口名称。

- `SOCAT_IP_LOCADDR`（输出）  
    对于应用了地址选项 `ip-pktinfo` 的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的接口地址。

- `SOCAT_IP_TOS`（输出）  
    对于应用了地址选项 `ip-recvtos` 的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的 TOS（服务类型）。

- `SOCAT_IP_TTL`（输出）  
    对于应用了地址选项 `ip-recvttl` 的所有基于 IPv4 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的 TTL（生存时间）。

- `SOCAT_IPV6_HOPLIMIT`（输出）  
    对于应用了地址选项 `ipv6-recvhoplimit` 的所有基于 IPv6 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的 hoplimit 值。

- `SOCAT_IPV6_DSTADDR`（输出）  
    对于应用了地址选项 `ipv6-recvpktinfo` 的所有基于 IPv6 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的目标地址。

- `SOCAT_IPV6_TCLASS`（输出）  
    对于应用了地址选项 `ipv6-recvtclass` 的所有基于 IPv6 的 `RECVFROM` 地址，`socat` 将此变量设置为接收数据包的传输类。

- `SOCAT_OPENSSL_X509_ISSUER`（输出）  
    对等证书中的颁发者字段。

- `SOCAT_OPENSSL_X509_SUBJECT`（输出）  
    对等证书中的主题字段。

- `SOCAT_OPENSSL_X509_COMMONNAME`（输出）  
    对等证书主题中的 `commonName` 条目。多个值由 “ // ” 分隔。

- `SOCAT_OPENSSL_X509_*`（输出）  
    对等证书主题中的所有其他条目。

- `SOCAT_OPENSSL_X509V3_DNS`（输出）  
    对等证书扩展中的 DNS 条目 - `subjectAltName` 字段。多个值由 “ // ” 分隔。

- `HOSTNAME`（输入）  
    用于确定日志记录的主机名（参见 `-lh`）。

- `LOGNAME`（输入）  
    如果未给出 `socksuser`，用作 socks 客户端用户名。使用选项 `su` 和 `su-d` 时，`LOGNAME` 设置为给定用户名。

- `USER`（输入）  
    如果未给出 `socksuser` 且 `LOGNAME` 为空，用作 socks 客户端用户名。使用选项 `su` 和 `su-d` 时，`USER` 设置为给定用户名。

- `SHELL`（输出）  
    使用选项 `su` 和 `su-d` 时，`SHELL` 设置为给定用户的登录 shell。

- `PATH`（输出）  
    可以通过 `exec`、`system` 和 `SHELL` 地址的选项 `path` 设置。

- `HOME`（输出）  
    使用选项 `su` 和 `su-d` 时，`HOME` 设置为给定用户的主目录。

## 致谢

以下小组和组织的工作对本项目非常宝贵：

*FSF*（GNU，[http://www.fsf.org/](http://www.fsf.org/)）项目及其自由且可移植的开发软件以及许多其他有用的工具和库。

*Linux 开发者社区*（[http://www.linux.org/](http://www.linux.org/)）提供自由开源操作系统。

*Open Group*（[http://www.unix-systems.org/](http://www.unix-systems.org/)）在 Internet 上免费提供其标准规范。

## 版本

本手册页描述 `socat` 版本 `1.8.1`。

## 缺陷

- 地址不能嵌套，因此单个 `socat` 进程不能例如在 socks 上驱动 ssl。

- 地址选项 `ftruncate` 不带值时使用默认值 `1` 而不是 `0`。

- 详细模式（`-x` 和/或 `-v`）在使用地址选项 `cr` 或 `crnl` 时显示行终止字符不一致：它们在任一方向上显示转换*之后*的数据。

- 数据传输块大小设置（`-b`）在地址 `readline` 下被忽略。

将错误报告发送到 `<socat@dest-unreach.org>`。

## 另请参阅

`nc(1)`、`rinetd(8)`、`openssl(1)`、`stunnel(8)`、`rlwrap(1)`、“setsid(1)”

`Socat` 主页 [http://www.dest-unreach.org/socat/](http://www.dest-unreach.org/socat/)

## 作者

Gerhard Rieger `<rieger@dest-unreach.org>` 及贡献者

## 版权页

本页是 *socat*（多用途中继（SOcket CAT））项目的一部分。项目信息可在 ⟨[http://www.dest-unreach.org/socat/](http://www.dest-unreach.org/socat/)⟩ 找到。目前不知道如何为此手册页报告错误；如果你知道，请发送邮件到 `man-pages@man7.org`。本页获取自 tarball `socat-1.8.1.3.tar.gz`，该 tarball 于 2026-08-04 从 ⟨[http://www.dest-unreach.org/socat/download/](http://www.dest-unreach.org/socat/download/)⟩ 获取。如果你发现此 HTML 版本页面有任何渲染问题，或认为有更好或更新的页面来源，或对本 COLOPHON 中的信息（这*不是*原始手册页的一部分）有更正或改进，请发送邮件到 `man-pages@man7.org`。

`socat(1)`

---

引用本页的页面：“systemd-socket-proxyd(8)”