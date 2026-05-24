
[文档](https://nmap.org/book/toc.html)
[在线扫描测试站点](http://scanme.nmap.org/)



## 名称
nmap — 网络探测工具和安全/端口扫描器

## 概要
`nmap` [ *`<Scan Type>`* ... ] [ *`<Options>`* ] { *`<target specification>`* }

## 描述

> **注意**：本文档介绍了可从 [`https://nmap.org/download.html`](https://nmap.org/download.html) 或 [`https://nmap.org/dist/?C=M&O=D`](https://nmap.org/dist/?C=M&O=D) 获取的 Nmap 最新版本。在报告某项功能未按描述工作之前，请确保您正在使用该最新版本。

Nmap（“网络映射器”）是一款用于网络探测和安全审计的开源工具。它被设计用于快速扫描大型网络，当然对单个主机的扫描也同样出色。Nmap 以创新的方式使用原始 IP 报文来发现网络上有哪些主机，这些主机提供什么服务（应用程序名称和版本），运行什么操作系统（及其版本），使用了何种报文过滤器/防火墙，以及许多其他特征。虽然 Nmap 通常用于安全审计，但许多系统和网络管理员发现它在日常工作中同样有用，例如网络资产盘点、管理服务升级计划以及监控主机或服务的正常运行时间。

Nmap 的输出是一个已扫描目标的列表，并根据所使用的选项提供每个目标的补充信息。这些信息中最关键的是“**感兴趣的端口表**”。该表列出了端口号、协议、服务名称和状态。状态可能是 `open`、`filtered`、`closed` 或 `unfiltered`。`open` 表示目标机器上的应用程序正在该端口上监听连接/报文。`filtered` 表示防火墙、过滤器或其他网络障碍正在阻塞该端口，导致 Nmap 无法判断它是 `open` 还是 `closed`。`closed` 端口没有应用程序监听，但它们随时可能开放。当端口对 Nmap 的探测有响应，但 Nmap 无法确定其是开放还是关闭时，端口会被归类为 `unfiltered`。当 Nmap 无法确定某个端口属于这两种状态中的哪一种时，会报告组合状态 `open|filtered` 和 `closed|filtered`。当请求了版本探测时，端口表还可能包含软件版本详情。当请求 IP 协议扫描（`-sO`）时，Nmap 会提供所支持的 IP 协议信息，而不是监听端口信息。

除了感兴趣的端口表之外，Nmap 还能提供关于目标的更多信息，包括反向 DNS 名称、操作系统猜测、设备类型和 MAC 地址。

一次典型的 Nmap 扫描如 **示例 15.1** 所示。此示例中使用的 Nmap 参数仅有 `-A`（启用操作系统和版本探测、脚本扫描和路由追踪）；`-T4`（用于更快执行）；以及目标主机名。

**示例 15.1. 一次典型的 Nmap 扫描**

```log
# nmap -A -T4 scanme.nmap.org

Nmap scan report for scanme.nmap.org (74.207.244.221)
Host is up (0.029s latency).
rDNS record for 74.207.244.221: li86-221.members.linode.com
Not shown: 995 closed ports
PORT     STATE    SERVICE     VERSION
22/tcp   open     ssh         OpenSSH 5.3p1 Debian 3ubuntu7 (protocol 2.0)
| ssh-hostkey: 1024 8d:60:f1:7c:ca:b7:3d:0a:d6:67:54:9d:69:d9:b9:dd (DSA)
|_2048 79:f8:09:ac:d4:e2:32:42:10:49:d3:bd:20:82:85:ec (RSA)
80/tcp   open     http        Apache httpd 2.2.14 ((Ubuntu))
|_http-title: Go ahead and ScanMe!
646/tcp  filtered ldp
1720/tcp filtered H.323/Q.931
9929/tcp open     nping-echo  Nping echo
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.39
OS details: Linux 2.6.39
Network Distance: 11 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:kernel

TRACEROUTE (using port 53/tcp)
HOP RTT      ADDRESS
[Cut first 10 hops for brevity]
11  17.65 ms li86-221.members.linode.com (74.207.244.221)

Nmap done: 1 IP address (1 host up) scanned in 14.40 seconds
```

最新版本的 Nmap 可从 [`https://nmap.org`](https://nmap.org) 获取。本手册页的最新版本可在 [`https://nmap.org/book/man.html`](https://nmap.org/book/man.html) 查阅。它也被收录为《*Nmap Network Scanning: The Official Nmap Project Guide to Network Discovery and Security Scanning*》的一章。

## 选项摘要

此选项摘要在不带任何参数运行 Nmap 时打印，最新版本始终可在 [https://svn.nmap.org/nmap/docs/nmap.usage.txt](https://svn.nmap.org/nmap/docs/nmap.usage.txt) 获取。它帮助人们记住最常用的选项，但不能替代本手册其余部分的深入文档。一些不常见的选项甚至未包含在此处。

```log
Nmap 7.99SVN ( https://nmap.org )
用法: nmap [扫描类型] [选项] {目标指定}
目标指定:
  可传递主机名、IP 地址、网络等。
  例: scanme.nmap.org, microsoft.com/24, 192.168.0.1; 10.0.0-255.1-254
  -iL <输入文件名>: 从主机/网络列表文件中输入
  -iR <主机数量>: 选择随机目标
  --exclude <主机1[,主机2][,主机3],...>: 排除主机/网络
  --excludefile <排除文件>: 从文件中获取排除列表
主机发现:
  -sL: 列表扫描 - 仅列出要扫描的目标
  -sn: Ping 扫描 - 禁用端口扫描
  -Pn: 将所有主机视为在线 -- 跳过主机发现
  -PS/PA/PU/PY[端口列表]: 对给定端口进行 TCP SYN、TCP ACK、UDP 或 SCTP 发现
  -PE/PP/PM: ICMP 回显、时间戳和网络掩码请求发现探测
  -PO[协议列表]: IP 协议 Ping
  -n/-R: 从不进行 DNS 解析/始终解析 [默认: 有时]
  --dns-servers <服务器1[,服务器2],...>: 指定自定义 DNS 服务器
  --system-dns: 使用操作系统的 DNS 解析器
  --traceroute: 追踪到每个主机的跃点路径
扫描技术:
  -sS/sT/sA/sW/sM: TCP SYN/Connect()/ACK/Window/Maimon 扫描
  -sU: UDP 扫描
  -sN/sF/sX: TCP Null、FIN 和 Xmas 扫描
  --scanflags <标志>: 自定义 TCP 扫描标志
  -sI <僵尸主机[:探测端口]>: 空闲扫描
  -sY/sZ: SCTP INIT/COOKIE-ECHO 扫描
  -sO: IP 协议扫描
  -b <FTP 中继主机>: FTP 反弹扫描
端口指定与扫描顺序:
  -p <端口范围>: 仅扫描指定端口
    例: -p22; -p1-65535; -p U:53,111,137,T:21-25,80,139,8080,S:9
  --exclude-ports <端口范围>: 将指定端口排除在扫描之外
  -F: 快速模式 - 扫描比默认扫描更少的端口
  -r: 顺序扫描端口 - 不随机化
  --top-ports <数量>: 扫描 <数量> 个最常见端口
  --port-ratio <比率>: 扫描比 <比率> 更常见的端口
服务/版本检测:
  -sV: 探测开放端口以确定服务/版本信息
  --version-intensity <级别>: 设置探测强度，从 0 (轻量) 到 9 (尝试所有探测)
  --version-light: 限制为最可能的探测 (强度 2)
  --version-all: 尝试每一个探测 (强度 9)
  --version-trace: 显示详细的版本扫描活动 (用于调试)
脚本扫描:
  -sC: 等同于 --script=default
  --script=<Lua 脚本>: <Lua 脚本> 是一个逗号分隔的列表，包含
           目录、脚本文件或脚本类别
  --script-args=<n1=v1,[n2=v2,...]>: 为脚本提供参数
  --script-args-file=文件名: 在文件中提供 NSE 脚本参数
  --script-trace: 显示所有发送和接收的数据
  --script-updatedb: 更新脚本数据库。
  --script-help=<Lua 脚本>: 显示关于脚本的帮助。
           <Lua 脚本> 是一个逗号分隔的脚本文件或脚本类别列表。
操作系统检测:
  -O: 启用操作系统检测
  --osscan-limit: 将操作系统检测限制在有希望的目标
  --osscan-guess: 更积极地猜测操作系统
时序与性能:
  接受 <时间> 的选项以秒为单位，或在值后附加 'ms' (毫秒)、's' (秒)、'm' (分钟) 或 'h' (小时) (例如 30m)。
  -T<0-5>: 设置时序模板 (越高越快)
  --min-hostgroup/max-hostgroup <大小>: 并行主机扫描组大小
  --min-parallelism/max-parallelism <探测数量>: 探测并行化
  --min-rtt-timeout/max-rtt-timeout/initial-rtt-timeout <时间>: 指定探测往返时间。
  --max-retries <尝试次数>: 限制端口扫描探测重传的最大次数。
  --host-timeout <时间>: 在此时间后放弃目标
  --scan-delay/--max-scan-delay <时间>: 调整探测之间的延迟
  --min-rate <数量>: 以不低于每秒 <数量> 的速度发送数据包
  --max-rate <数量>: 以不高于每秒 <数量> 的速度发送数据包
防火墙/IDS 规避与欺骗:
  -f; --mtu <值>: 分片数据包 (可选 w/给定 MTU)
  -D <诱饵1,诱饵2[,ME],...>: 用诱饵伪装扫描
  -S <IP_地址>: 伪造源地址
  -e <接口>: 使用指定接口
  -g/--source-port <端口号>: 使用给定端口号
  --proxies <url1,[url2],...>: 通过 HTTP/SOCKS4 代理中继连接
  --data <十六进制字符串>: 向发送的数据包附加自定义负载
  --data-string <字符串>: 向发送的数据包附加自定义 ASCII 字符串
  --data-length <数量>: 向发送的数据包附加随机数据
  --ip-options <选项>: 发送带有指定 IP 选项的数据包
  --ttl <值>: 设置 IP 生存时间字段
  --spoof-mac <MAC 地址/前缀/供应商名称>: 伪造你的 MAC 地址
  --badsum: 发送带有伪造 TCP/UDP/SCTP 校验和的数据包
输出:
  -oN/-oX/-oS/-oG <文件>: 分别以正常、XML、脚本小子和 Grepable 格式将扫描结果输出到给定文件名。
  -oA <基本文件名>: 一次性以三种主要格式输出
  -v: 提高详细程度 (使用 -vv 或更多以获得更大效果)
  -d: 提高调试级别 (使用 -dd 或更多以获得更大效果)
  --reason: 显示端口处于特定状态的原因
  --open: 仅显示开放的 (或可能开放的) 端口
  --packet-trace: 显示所有发送和接收的数据包
  --iflist: 打印主机接口和路由 (用于调试)
  --append-output: 附加到而非覆盖指定的输出文件
  --resume <文件名>: 恢复已中止的扫描
  --noninteractive: 禁用通过键盘的运行时交互
  --stylesheet <路径/URL>: 用于将 XML 输出转换为 HTML 的 XSL 样式表
  --webxml: 引用来自 Nmap.Org 的样式表以获得更可移植的 XML
  --no-stylesheet: 防止 XSL 样式表与 XML 输出关联
杂项:
  -6: 启用 IPv6 扫描
  -A: 启用操作系统检测、版本检测、脚本扫描和路由追踪
  --datadir <目录名>: 指定自定义 Nmap 数据文件位置
  --send-eth/--send-ip: 使用原始以太网帧或 IP 数据包发送
  --privileged: 假定用户具有完全特权
  --unprivileged: 假定用户缺少原始套接字特权
  -V: 打印版本号
  -h: 打印此帮助摘要页面。
示例:
  nmap -v -A scanme.nmap.org
  nmap -v -sn 192.168.0.0/16 10.0.0.0/8
  nmap -v -iR 10000 -Pn -p 80
更多选项和示例请参见手册页 (https://nmap.org/book/man.html)
```


## Atips

- 主要功能为端口探测 + 信息脚本探测
- 默认行为
    - 扫描 TCP 开放端口
    - 扫描常见端口列表
    - 使用该特定端口的最常见应用程序的名称
- 常用命令参数
    - 参数
        - `sV` 探测开放端口以识别服务/版本信息
    - 主机发现:
        默认情况下，Nmap 会进行主机发现，然后对每个确定在线的主机执行端口扫描。
        - `-sn` 
            不进行端口扫描
        - `-Pn` 
            忽略对主机的初始 ping 扫描，由于 ICMP 包可能已被防火墙阻止
        - `-n` 
            不进行 DNS 解析
    - 扫描技术
        - `sT` TCP 连接扫描
        - `sU` UDP 扫描
    - 端口规范和扫描顺序
        - `-p<端口范围>`  
            仅扫描指定端口。可以单独指定端口编号，也可以使用连字符分隔的范围（例如 1-1023）
            - `-p-` 扫描所有端口
    - 脚本
        - 脚本目录 `/usr/share/nmap/scripts/`
        - 使用 `and`、`or` 和 `not` 运算符构建布尔表达式来进行更复杂的脚本选择
    - 详细级别和调试选项：
        - `-v`
            增加详细级别
        - `--open`  
            仅显示开放（或可能开放）的端口
    - 输出
        - `-oN/-oX/-oS/-oG <文件>` 分别以正常、XML、脚本小子风格和 Grepable 格式保存扫描输出
    - 时间和性能：
        - `-T paranoid|sneaky|polite|normal|aggressive|insane`  
            六种时间模板允许用户指定他们希望采取的攻击强度: 偏执狂（0）、鬼祟（1）、礼貌（2）、正常（3）、侵略（4）和疯狂（5）。
            前两种用于入侵检测系统（IDS）规避。
            礼貌模式会减慢扫描速度以减少带宽和目标机器资源的使用。
            正常模式是默认设置，所以-T3 不会产生任何效果。
            侵略模式通过假设你处于一个相当快且可靠的网络上来加速扫描。
            最后是疯狂模式，它假设你处于一个异常快的网络上，或者愿意为了速度牺牲一些准确性。
    - 杂项
        - `-A`（激进扫描选项）
            此选项可启用额外的高级和激进功能。目前，它会启用操作系统检测（-O）、版本扫描（-sV）、脚本扫描（-sC）和路由追踪（--traceroute）。未来可能会增加更多功能。其目的是启用一套全面的扫描选项，而无需用户记住大量的标志，默认脚本扫描被认为具有侵入性。此选项仅启用功能，不会启用你可能同样需要的计时选项（如 -T4）或详细输出选项（-v）。需要特权（如 root 访问权限）的选项（如操作系统检测和路由追踪）仅在这些特权可用时才会被启用。


- 空闲扫描
  - 使用 MSF 框架的 `auxiliary/scanner/ip/ipidseq` 定位可执行空闲扫描的主机
  - 使用 Nmap 的 `-sI 僵尸主机 目标ip` 空闲扫描选项
