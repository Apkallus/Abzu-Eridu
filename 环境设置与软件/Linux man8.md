## service — 运行 System V 初始化脚本

## 概要
`service SCRIPT COMMAND [OPTIONS]`
`service --status-all`
`service --help | -h | --version`

## 描述
`service` 在一个尽可能可预测的环境中运行 System V 初始化脚本，它移除了大部分环境变量，并将当前工作目录设置为 `/`。
SCRIPT 参数指定一个位于 `/etc/init.d/SCRIPT` 的 System V 初始化脚本。所支持的 COMMAND 值取决于被调用的脚本，`service` 会将 COMMAND 及 OPTIONS 原样传递给该初始化脚本。所有脚本至少应支持 `start` 和 `stop` 命令。一种特殊情况是：当 COMMAND 为 `--full-restart` 时，该脚本会运行两次——先以 `stop` 命令运行，再以 `start` 命令运行。

`service --status-all` 会按字母顺序对所有初始化脚本执行 `status` 命令。

## 文件
`/etc/init.d`  
存放 System V 初始化脚本的目录。

## 环境变量
`LANG`, `TERM`  
仅有的两个会传递给初始化脚本的环境变量。

## netstat - 打印网络连接、路由表、接口统计、伪装连接和多播成员信息  

**概要**  
`netstat [地址族选项] [--tcp|-t] [--udp|-u] [--udplite|-U] [--sctp|-S] [--raw|-w] [--l2cap|-2] [--rfcomm|-f] [--listening|-l] [--all|-a] [--numeric|-n] [--numeric-hosts] [--numeric-ports] [--numeric-users] [--symbolic|-N] [--extend|-e|-ee] [--timers|-o] [--program|-p] [--verbose|-v] [--continuous|-c] [--wide|-W]`  

`netstat {--route|-r} [地址族选项] [--extend|-e|-ee] [--verbose|-v] [--numeric|-n] [--numeric-hosts] [--numeric-ports] [--numeric-users] [--continuous|-c]`  

`netstat {--interfaces|-i} [--all|-a] [--extend|-e] [--numeric|-n] [--numeric-hosts] [--continuous|-c]`  

`netstat {--groups|-g} [--numeric|-n] [--numeric-hosts] [--numeric-ports] [--numeric-users] [--continuous|-c]`  

`netstat {--masquerade|-M} [--extend|-e] [--numeric|-n] [--numeric-hosts] [--numeric-ports] [--numeric-users] [--continuous|-c]`  

`netstat {--statistics|-s} [--tcp|-t] [--udp|-u] [--udplite|-U] [--sctp|-S] [--raw|-w]`  

`netstat {--version|-V}`  
`netstat {--help|-h}`  

`地址族选项：`  
`[-4|--inet] [-6|--inet6] [--protocol={inet,inet6,unix,ipx,ax25,netrom,ddp,bluetooth,...}] [--unix|-x] [--inet|--ip] [--ax25] [--x25] [--rose] [--ash] [--bluetooth] [--ipx] [--netrom] [--ddp|--appletalk] [--econet|--ec]`

**注意**  
本程序基本已过时。`netstat` 的替代品是 `ss`。`netstat -r` 的替代品是 `ip route`。`netstat -i` 的替代品是 `ip -s link`。`netstat -g` 的替代品是 `ip maddr`。

**描述**  
`netstat` 打印 Linux 网络子系统的信息。

**调用模式**  
打印的信息类型由第一个参数控制，如下所示：

`(无参数)` 默认情况下，`netstat` 显示已打开套接字的列表。如果不指定任何地址族，则会打印所有已配置地址族的活跃套接字。

`--route, -r` 显示内核路由表。详细信息请参见 `route(8)` 中的描述。`netstat -r` 与 `route -e` 输出相同。

`--groups, -g` 显示 IPv4 和 IPv6 的多播组成员信息。

`--interfaces, -i` 显示所有网络接口及其各自接收和发送错误计数器的表格。若不使用 `--extended` 选项，其输出与 `ifconfig -s` 相同，否则显示详细列表。

`--masquerade, -M` 显示伪装连接列表。

`--statistics, -s` 显示每个协议的摘要（SNMP）统计信息。

## ip —— 显示 / 操作路由、网络设备、接口和隧道

### 概要
`ip [ 选项 ] 对象 { 命令 | help }`

`ip [ -force ] -batch 文件名`

对象（OBJECT）可以是：  
`address` | `addrlabel` | `fou` | `help` | `ila` | `ioam` | `l2tp` |  
`link` | `macsec` | `maddress` | `monitor` | `mptcp` | `mroute` |  
`mrule` | `neighbor` | `neighbour` | `netconf` | `netns` | `nexthop` |  
`ntable` | `ntbl` | `route` | `rule` | `sr` | `tap` | `tcpmetrics` |  
`token` | `tunnel` | `tuntap` | `vrf` | `xfrm`  
*（注：对象名称可完整拼写或使用缩写，如 `address` 可缩写成 `addr` 或 `a`）*

选项（OPTIONS）包括：  
`-V[ersion]` | `-h[uman-readable]` | `-s[tatistics]` |  
`-d[etails]` | `-r[esolve]` | `-iec` |  
`-f[amily] { inet | inet6 | link }` | `-4` | `-6` | `-B` | `-0` |  
`-l[oops] [最大地址刷新尝试次数]` | `-o[neline]` | `-rc[vbuf] [大小]` |  
`-t[imestamp]` | `-ts[hort]` | `-n[etns] 名称` | `-N[umeric]` |  
`-a[ll]` | `-c[olor]` | `-br[ief]` | `-j[son]` | `-p[retty]`

---

### 选项详细说明

**-V**， **-Version**  
 打印 `ip` 工具的版本信息并退出。

**-h**， **-human**， **-human-readable**  
 以人类易读的格式输出统计信息，数值后附加单位后缀（如 K、M、G）。

**-b**， **-batch** <*文件名*>  
 从指定的文件或标准输入中读取命令并按顺序执行。遇到第一个错误时 `ip` 会终止执行。

**-force**  
 在批处理模式下即使遇到错误也不终止 `ip`。如果执行过程中发生任何错误，应用程序的返回值将为非零。

**-s**， **-stats**， **-statistics**  
 输出更多统计信息。该选项可多次使用，每多用一次，输出的信息量就增加一级。通常输出的是统计数据或时间相关数值。

**-d**， **-details**  
 输出更详细的信息。

**-l**， **-loops** <*次数*>  
 指定 `ip address flush` 逻辑在放弃之前尝试的最大循环次数。默认值为 10。设为 0 表示无限循环，直到所有地址被移除为止。

**-f**， **-family** <*协议族*>  
 指定使用的协议族。协议族标识符可以是 `inet`、`inet6`、`bridge`、`mpls` 或 `link` 之一。  
 如果未提供此选项，`ip` 会尝试从其他参数中推断协议族。若命令行其余部分无法提供足够信息，则回退到默认值，通常为 `inet` 或 `any`。  
 `link` 是特殊的协议族标识符，表示不涉及任何网络层协议（仅链路层）。

**-4**  
 等同于 `-family inet`。（IPv4）

**-6**  
 等同于 `-family inet6`。（IPv6）

**-B**  
 等同于 `-family bridge`。（桥接）

**-M**  
 等同于 `-family mpls`。（多协议标签交换）

**-0**  
 等同于 `-family link`。（链路层）

**-o**， **-oneline**  
 将每条记录输出为单行，用 `\` 字符替代换行符。当你需要配合 `wc(1)` 统计行数或 `grep(1)` 过滤输出时，该选项十分方便。

**-r**， **-resolve**  
 使用系统的名称解析器，尽可能以 DNS 名称代替 IP 地址进行显示。

**-n**， **-netns** <*网络命名空间名称*>  
 将 `ip` 切换到指定的网络命名空间执行。实际上，它简化了从  
 `ip netns exec NETNS ip [ 选项 ] 对象 { 命令 | help }`  
 到  
 `ip -n[etns] NETNS [ 选项 ] 对象 { 命令 | help }`  
 的书写方式。

**-N**， **-Numeric**  
 直接打印协议号、作用域、区分服务字段（dsfield）等的原始数值，而不将其转换为人类可读的名称。

**-a**， **-all**  
 对所有对象执行指定的命令。该选项是否生效取决于具体命令是否支持它。

**-c**[**color**][**=**{**always**|**auto**|**never**}]  
 配置彩色输出。若省略参数或设为 `always`，则无论标准输出是否指向终端都启用彩色；若为 `auto`，则仅在标准输出为终端时才启用彩色；若为 `never`，则禁用彩色。多次指定时以最后一次为准。  
 *注：若同时提供了 `-json` 选项，颜色标志会被忽略。*  
 所使用的调色板可受 `COLORFGBG` 环境变量影响（参见环境变量节）。

**-t**， **-timestamp**  
 在使用 `monitor` 选项时，显示每条记录产生时的当前时间戳。

**-ts**， **-tshort**  
 与 `-timestamp` 类似，但使用更短的日期时间格式。

**-rc**， **-rcvbuf**<*大小*>  
 设置 netlink 套接字的接收缓冲区大小，默认为 1MB。

**-iec**  
 以 IEC 标准单位（如 1Ki = 1024）打印人类可读的速率值。

**-br**， **-brief**  
 以表格形式只输出基本信息，提高可读性。该选项目前仅支持 `ip addr show`、`ip link show` 和 `ip neigh show` 命令。

**-j**， **-json**  
 以 JSON（JavaScript Object Notation）格式输出结果。

**-p**， **-pretty**  
 默认 JSON 格式紧凑但不易阅读。使用该标志会增加缩进换行，使输出格式化，便于阅读。

**-echo**  
 请求内核将应用后的配置内容回显到标准输出。

---

### IP 命令语法

**对象 (OBJECT)**  
 对象指定了命令要操作的实体类型。所有对象名均可使用全称或缩写形式。

*   **address** — 设备上的 IP（或 IPv6）地址。
*   **addrlabel** — 用于协议地址选择的标签配置。
*   **fou** — Foo-over-UDP 的接收端口配置。
*   **ila** — 管理标识符定位符地址（Identifier Locator Address）。
*   **ioam** — 管理 IOAM 命名空间和模式。
*   **l2tp** — 基于 IP 的以太网隧道（L2TPv3）。
*   **link** — 网络设备（接口）。
*   **macsec** — MACsec 设备配置。
*   **maddress** — 多播地址。
*   **monitor** — 监听并显示 netlink 消息（状态变化）。
*   **mptcp** — 管理 MPTCP 路径管理器。
*   **mroute** — 多播路由缓存条目。
*   **mrule** — 多播路由策略数据库中的规则。
*   **neighbor / neighbour** — 管理 ARP 或 NDISC 缓存条目。
*   **netconf** — 网络配置监控。
*   **netns** — 管理网络命名空间。
*   **nexthop** — 管理下一跳对象。
*   **ntable** — 管理邻居缓存的操作参数。
*   **route** — 路由表条目。
*   **rule** — 路由策略数据库中的规则。
*   **sr** — 管理 IPv6 段路由（Segment Routing）。
*   **stats** — 管理和显示接口统计信息。
*   **tcp_metrics / tcpmetrics** — 管理 TCP 度量信息。
*   **token** — 管理令牌化的接口标识符。
*   **tunnel** — 基于 IP 的隧道。
*   **tuntap** — 管理 TUN/TAP 虚拟设备。
*   **vrf** — 管理虚拟路由转发设备。
*   **xfrm** — 管理 IPSec 安全策略。

**命令 (COMMAND)**  
 指定对对象执行的操作。可用的操作取决于对象类型。一般来说，都支持 `add`（添加）、`delete`（删除）和 `show` 或 `list`（显示/列出），但部分对象不支持全部操作，或拥有额外的特殊命令。  
 所有对象都支持 `help` 命令，它会打印出该对象可用的命令列表及其参数语法。  
 如果没有给出任何命令，通常会假定一个默认命令（通常是 `list`；如果该类对象不能列出，则默认为 `help`）。

---

### 环境变量

**COLORFGBG**  
 如果设置了该变量，`ip` 会用它的值来判断终端背景是深色还是浅色，并据此选择对比度合适的颜色。  
 该变量通常包含两个或三个分号分隔的数值；`ip` 会使用其中最后一个数值。若最后一个数值是 0-6 或 8，则会选用适合深色背景的颜色方案。  
 示例：`COLORFGBG=";0" ip -c a` 会强制以深色背景风格显示彩色地址信息。

---

### 退出状态
*   **0** — 命令执行成功。
*   **1** — 命令行语法错误。
*   **2** — 内核报告错误（配置无法应用）。

---

### 示例

*   **ip addr**  
     显示所有网络接口上已配置的地址。
*   **ip neigh**  
     显示内核当前的邻居表（ARP/NDISC 缓存）。
*   **ip link set eth0 up**  
     启用网络接口 eth0。
*   **ip link set eth0 down**  
     禁用网络接口 eth0。
*   **ip route**  
     显示主路由表内容。