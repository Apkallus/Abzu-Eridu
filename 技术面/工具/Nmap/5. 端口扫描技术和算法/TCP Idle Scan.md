# TCP 空闲扫描（`-sI`）

> **注意**：志愿者已将本节翻译为[西班牙语](https://nmap.org/idlescan-es.html)和[葡萄牙语（巴西）](https://nmap.org/idlescan-pt-br.html)。

1998 年，安全研究员 Antirez（也是本书中使用的 hping2 工具的编写者）在 Bugtraq 邮件列表中发布了一种巧妙的新端口扫描技术。这项后来被称为“空闲扫描”的技术允许完全盲扫。攻击者实际上可以扫描目标而不从其自己的 IP 地址发送单个数据包！相反，一种巧妙的侧信道攻击允许扫描通过一个“僵尸主机”反弹。入侵检测系统的报告会将无辜的僵尸误认为是攻击者。除了极其隐蔽之外，这种扫描类型还可以发现机器之间基于 IP 的信任关系。

虽然空闲扫描比目前讨论的任何技术都要复杂，但你不需要成为 TCP/IP 专家就能理解它。它可以从以下基本事实组合而成：

- 确定 TCP 端口是否开放的一种方法是向该端口发送 SYN（会话建立）数据包。如果端口开放，目标机器将响应 SYN/ACK（会话请求确认）数据包；如果端口关闭，则响应 RST（重置）。这是先前讨论的 SYN 扫描的基础。
- 收到未经请求的 SYN/ACK 数据包的机器将响应 RST。未经请求的 RST 将被忽略。
- 互联网上的每个 IP 数据包都有一个分片标识号（IP ID）。由于许多操作系统只是为它们发送的每个数据包递增该编号，因此探测 IPID 可以告诉攻击者自上次探测以来已发送了多少数据包。

通过结合这些特性，可以在伪造身份的同时扫描目标网络，使得看起来像一个无辜的僵尸机器执行了扫描。

## 空闲扫描分步说明

从根本上说，空闲扫描包括三个步骤，每个端口重复执行：

1. 探测僵尸的 IP ID 并记录。
2. 从僵尸伪造一个 SYN 数据包，并将其发送到目标上的所需端口。根据端口状态，目标的反应可能导致或不会导致僵尸的 IP ID 递增。
3. 再次探测僵尸的 IP ID。然后通过将新的 IP ID 与步骤 1 中记录的 IP ID 进行比较来确定目标端口状态。

这个过程之后，僵尸的 IP ID 应该增加了 1 或 2。增加 1 表示僵尸除了响应攻击者的探测之外没有发送任何数据包。这种没有发送数据包的情况意味着端口未开放（目标必须向僵尸发送了一个 RST 数据包（被忽略）或什么也没发送）。增加 2 表示僵尸在两次探测之间发送了一个数据包。这个额外的数据包通常意味着端口是开放的（目标可能响应伪造的 SYN 向僵尸发送了一个 SYN/ACK 数据包，从而诱导僵尸发送 RST 数据包）。增加大于 2 通常表示僵尸主机不好，可能没有可预测的 IP ID 编号，或者可能参与了与空闲扫描无关的通信。

尽管关闭端口发生的情况与过滤端口略有不同，但攻击者在两种情况下测量到的结果相同，即 IP ID 增加 1。因此，空闲扫描无法区分关闭端口和过滤端口。当 Nmap 记录到 IP ID 增加 1 时，它将端口标记为 `closed|filtered`。

对于想要更多细节的人，以下三个图表准确显示了在开放、关闭和过滤端口三种情况下发生的情况。每个图中的角色是：攻击者、僵尸、目标。

**图 5.6. 开放端口的空闲扫描**

![图 5.6](images/idle-scan-open.png)
*步骤 1：攻击者向僵尸发送 SYN/ACK。僵尸没有预期到 SYN/ACK，发回一个 RST，泄露其 IP ID。步骤 2：目标响应看似来自僵尸的 SYN，发送 SYN/ACK。僵尸没有预期到它，发回一个 RST，在此过程中递增其 IP ID。自步骤 1 以来僵尸的 IP ID 增加了 2，因此端口是开放的！*

**图 5.7. 关闭端口的空闲扫描**

![图 5.7](images/idle-scan-closed.png)
*步骤 1：攻击者向僵尸发送 SYN/ACK。僵尸没有预期到 SYN/ACK，发回一个 RST，泄露其 IP ID。此步骤始终相同。步骤 2：目标响应看似来自僵尸的 SYN，发送 RST（端口关闭）。僵尸忽略未经请求的 RST，其 IP ID 不变。步骤 3：自步骤 1 以来僵尸的 IP ID 仅增加了 1，因此端口未开放。*

**图 5.8. 过滤端口的空闲扫描**

![图 5.8](images/idle-scan-filtered.png)
*步骤 1：与其他两种情况一样，攻击者向僵尸发送 SYN/ACK。僵尸泄露其 IP ID。步骤 2：目标顽固地过滤其端口，忽略看似来自僵尸的 SYN。僵尸不知道发生了什么，没有递增其 IP ID。步骤 3：自步骤 1 以来僵尸的 IP ID 仅增加了 1，因此端口未开放。从攻击者的角度来看，这个过滤端口与关闭端口无法区分。*

空闲扫描是终极的隐蔽扫描。Nmap 提供诱饵扫描（`-D`）来帮助用户隐藏身份，但（与空闲扫描不同）这仍然需要攻击者从其真实 IP 地址向目标发送一些数据包以获取扫描结果。空闲扫描的一个结果是入侵检测系统通常会发出警报，声称僵尸机器已对它们发起扫描。因此，它可用于将扫描行为嫁祸给其他方。在阅读 IDS 的警报时请记住这种可能性。

空闲扫描的一个独特优势是它可以用来绕过某些数据包过滤防火墙和路由器。IP 源地址过滤是一种常见（但较弱）的安全机制，用于限制可以连接到敏感主机或网络的机器。例如，公司数据库服务器可能只允许访问它的公共 Web 服务器连接。或者家庭用户可能只允许从其工作机器进行 SSH（交互式登录）连接。

更令人不安的情况是，当某公司高管要求网络管理员打开防火墙漏洞，以便他可以从家庭 IP 地址访问内部网络资源时。当高管不愿意或无法使用安全的 VPN 替代方案时，就可能发生这种情况。

空闲扫描有时可用于映射这些信任关系。关键因素是空闲扫描结果列出了从僵尸主机视角看到的开放端口。对前述数据库服务器进行正常扫描可能显示没有开放端口，但使用 Web 服务器的 IP 作为僵尸执行空闲扫描可能会显示数据库相关服务端口为开放，从而暴露信任关系。

映射这些信任关系对攻击者优先确定目标非常有用。上面讨论的 Web 服务器对攻击者来说可能看起来很普通，直到她注意到其特殊的数据库访问权限。

空闲扫描的一个缺点是它比大多数其他扫描类型花费的时间长得多。尽管有优化的算法，一个 15 秒的 SYN 扫描作为空闲扫描可能需要 15 分钟或更长时间。另一个问题是，你必须能够伪造数据包，使其看起来像是来自僵尸并到达目标机器。现在许多 ISP（尤其是拨号和住宅宽带提供商）实施出口过滤以防止这种数据包伪造。高端提供商（如托管和 T1 服务）不太可能这样做。如果启用了这种过滤，Nmap 会为你尝试的每个僵尸打印一条快速错误消息。如果无法更换 ISP，你可以尝试使用同一 ISP 网络上的另一个 IP。有时过滤只阻止来自客户使用范围*之外*的 IP 地址的欺骗。空闲扫描的另一个挑战是你必须找到一个可用的僵尸主机，如下一节所述。

## 寻找可用的空闲扫描僵尸主机

执行 IP ID 空闲扫描的第一步是找到合适的僵尸。它需要以全局（而不是基于与之通信的每个主机）的方式增量分配 IP ID 数据包。它应该是空闲的（因此得名扫描），因为无关的流量会增加其 IP ID 序列，混淆扫描逻辑。攻击者与僵尸之间、僵尸与目标之间的延迟越低，扫描速度越快。

当尝试空闲扫描时，Nmap 会测试提议的僵尸并报告任何问题。如果一个不起作用，请尝试另一个。有足够多的互联网主机易受攻击，僵尸候选并不难找到。由于主机需要空闲，选择知名主机如 www.yahoo.com 或 google.com 几乎永远不会成功。

一种常见的方法是对某个网络执行 Nmap ping 扫描。你可以使用 Nmap 的随机 IP 选择模式（`-iR`），但这可能导致距离很远、延迟很大的僵尸。选择靠近源地址或靠近目标的网络会产生更好的结果。你可以尝试使用 ping 扫描结果中的每个可用主机进行空闲扫描，直到找到一个有效的。像往常一样，最好在将他人的机器用于意外目的（如空闲扫描）之前获得许可。

我们在插图中选择打印机图标来表示僵尸不仅仅是为了有趣——简单的网络设备通常是很棒的僵尸，因为它们通常既未充分利用（空闲）又具有容易受到 IP ID 流量检测的简单网络堆栈。

对僵尸候选网络执行端口扫描和操作系统识别（`-O`）而不仅仅是 ping 扫描有助于选择好的僵尸。只要启用了详细模式（`-v`），操作系统检测通常会确定 IP ID 序列生成方法并打印一行，如“IP ID Sequence Generation: Incremental”。如果类型显示为 `Incremental` 或 `Broken little-endian incremental`，则该机器是一个不错的僵尸候选。这仍然不能保证它有效，因为 Solaris 和其他一些系统为它们通信的每个主机创建一个新的 IP ID 序列。主机也可能太忙。操作系统检测和开放端口列表也有助于识别可能空闲的系统。

另一种识别僵尸候选的方法是针对主机运行 `ipidseq` NSE 脚本。该脚本探测主机以分类其 IP ID 生成方法，然后打印 IP ID 分类，与操作系统检测非常相似。与大多数 NSE 脚本一样，`ipidseq.nse` 可以并行对许多主机运行，使其成为扫描整个网络寻找合适主机时的另一个好选择。

虽然识别合适的僵尸需要一些初始工作，但你可以继续重复使用好的僵尸。

## 执行空闲扫描

一旦找到合适的僵尸，执行扫描就很容易了。只需将僵尸主机名指定给 `-sI` 选项，Nmap 就会完成其余工作。示例 5.19 显示了 Ereet 通过对 Adobe 机器 Kiosk 进行空闲扫描反弹来扫描美国唱片工业协会（RIAA）的示例。

**示例 5.19. 针对 RIAA 的空闲扫描**

```bash
# nmap -Pn -p- -sI kiosk.adobe.com www.riaa.com

Starting Nmap ( https://nmap.org )
Idlescan using zombie kiosk.adobe.com (192.150.13.111:80); Class: Incremental
Nmap scan report for 208.225.90.120
(The 65522 ports scanned but not shown below are in state: closed)
Port       State       Service
21/tcp     open        ftp
25/tcp     open        smtp
80/tcp     open        http
111/tcp    open        sunrpc
135/tcp    open        loc-srv
443/tcp    open        https
1027/tcp   open        IIS
1030/tcp   open        iad1
2306/tcp   open        unknown
5631/tcp   open        pcanywheredata
7937/tcp   open        unknown
7938/tcp   open        unknown
36890/tcp  open        unknown

Nmap done: 1 IP address (1 host up) scanned in 2594.47 seconds
```

从上面的扫描中，我们了解到 RIAA 不太注重安全性（注意开放的 PC Anywhere、portmapper 和 Legato nsrexec 端口）。由于它们显然没有防火墙，它们很可能也没有 IDS。但如果有，它会显示 kiosk.adobe.com 是扫描的罪魁祸首。`-Pn` 选项阻止 Nmap 向 RIAA 机器发送初始 ping 数据包。否则会泄露 Ereet 的真实地址。扫描花了很长时间，因为指定了 `-p-` 来扫描全部 65K 个端口。不要尝试使用 kiosk 进行扫描，因为它已经被移除了。

默认情况下，Nmap 从僵尸的源端口 80 伪造探测数据包到目标。你可以通过在僵尸名称后附加冒号和端口号来选择不同的端口（例如 `-sI kiosk.adobe.com:113`）。选择的端口必须不被攻击者或目标过滤。对僵尸的 SYN 扫描应显示该端口处于 `open` 或 `closed` 状态。

## 空闲扫描实现算法

虽然“空闲扫描分步说明”一节从根本上描述了空闲扫描，但 Nmap 的实现要复杂得多。关键区别在于并行性以实现快速执行和冗余以减少误报。

由于推断端口状态的间接方法，并行化空闲扫描比其他扫描技术更棘手。如果 Nmap 向目标上的许多端口发送探测，然后检查僵尸的新 IP ID 值，那么 IP ID 的增量将暴露有多少目标端口是开放的，但不能暴露哪些端口。这实际上并不是一个大问题，因为大规模扫描中的绝大多数端口将是 `closed|filtered`。由于只有开放端口导致 IP ID 值递增，Nmap 将看不到中间的增量，并可以将整个端口组标记为 `closed|filtered`。Nmap 可以并行扫描多达 100 个端口的组。如果 Nmap 探测一个组后发现僵尸 IP ID 增加了 `<N>` 次，那么该组中一定有 `<N>` 个开放端口。然后 Nmap 通过二分搜索找到开放端口。它将组分成两个，并分别向每个子组发送探测。如果一个子组显示零个开放端口，则该子组的所有端口都被标记为 `closed|filtered`。如果一个子组显示一个或多个开放端口，则再次分割该子组，并继续该过程，直到识别出这些端口。虽然这种技术增加了复杂性，但它可以将扫描时间减少一个数量级，相比一次只扫描一个端口。

可靠性是空闲扫描的另一个主要问题。如果僵尸主机在扫描期间向任何无关机器发送数据包，其 IP ID 会递增。这导致 Nmap 认为它发现了一个开放端口。幸运的是，并行扫描在这里也有帮助。如果 Nmap 扫描一组 100 个端口，并且 IP ID 增加信号显示两个开放端口，Nmap 将组分成两个 50 端口的子组。当 Nmap 对两个子组进行 IP ID 扫描时，僵尸 IP ID 的总增加量必须再次为 2！否则，Nmap 将检测到不一致并重新扫描这些组。它还会根据检测到的僵尸的可靠性率修改组大小和扫描计时。如果 Nmap 检测到太多不一致的结果，它将退出并要求用户提供更好的僵尸。

有时数据包跟踪是理解这些复杂算法和技术的最佳方式。同样，Nmap 的 `--packet-trace` 选项可以在需要时轻松生成这些跟踪。本节的其余部分提供了一个实际七端口空闲扫描的带注释数据包跟踪。IP 地址已更改为 `Attacker`、`Zombie` 和 `Target`，并且为了清晰起见，删除了跟踪行中一些不相关的方面（例如 TCP 窗口大小）。

```bash
Attacker# nmap -sI Zombie -Pn -p20-25,110 -r --packet-trace -v Target
Starting Nmap ( https://nmap.org )
```

`-Pn` 对于隐蔽性是必要的，否则将从攻击者的真实地址向目标发送 ping 数据包。版本扫描也会暴露真实地址，因此*不*指定 `-sV`。`-r` 选项（关闭端口随机化）仅用于使本示例更易于理解。

Nmap 首先通过向 Zombie 发送六个 SYN/ACK 数据包并分析响应来测试 Zombie 的 IP ID 序列生成。这有助于 Nmap 立即淘汰坏的僵尸。这也是必要的，因为某些系统（通常是 Microsoft Windows 机器，尽管并非所有 Windows 都这样）为每个发送的数据包将 IP ID 增加 256 而不是 1。这发生在小端机器上，当它们没有将 IP ID 转换为网络字节序（大端）时。Nmap 使用这些初始探测来检测并解决此问题。

```
SENT (0.0060s) TCP Attacker:51824 > Zombie:80 SA id=35996
SENT (0.0900s) TCP Attacker:51825 > Zombie:80 SA id=25914
SENT (0.1800s) TCP Attacker:51826 > Zombie:80 SA id=39591
RCVD (0.1550s) TCP Zombie:80 > Attacker:51824 R id=15669
SENT (0.2700s) TCP Attacker:51827 > Zombie:80 SA id=43604
RCVD (0.2380s) TCP Zombie:80 > Attacker:51825 R id=15670
SENT (0.3600s) TCP Attacker:51828 > Zombie:80 SA id=34186
RCVD (0.3280s) TCP Zombie:80 > Attacker:51826 R id=15671
SENT (0.4510s) TCP Attacker:51829 > Zombie:80 SA id=27949
RCVD (0.4190s) TCP Zombie:80 > Attacker:51827 R id=15672
RCVD (0.5090s) TCP Zombie:80 > Attacker:51828 R id=15673
RCVD (0.5990s) TCP Zombie:80 > Attacker:51829 R id=15674
Idlescan using zombie Zombie (Zombie:80); Class: Incremental
```

该测试表明僵尸工作正常。每个 IP ID 都比前一个增加 1。因此系统似乎是空闲的，并且容易受到 IP ID 流量检测。这些有希望的结果仍需接受下一个测试，其中 Nmap 伪造四个数据包发送给 Zombie，就好像它们来自 Target。然后它探测僵尸以确保 IP ID 增加了。如果没有增加，则可能是攻击者的 ISP 阻止了伪造数据包，或者僵尸为它通信的每个主机使用单独的 IP ID 序列计数器。这两种情况都很常见，因此 Nmap 总是执行此测试。如上所示，最后已知的 Zombie IP ID 是 15674。

```
SENT (0.5990s) TCP Target:51823 > Zombie:80 SA id=1390
SENT (0.6510s) TCP Target:51823 > Zombie:80 SA id=24025
SENT (0.7110s) TCP Target:51823 > Zombie:80 SA id=15046
SENT (0.7710s) TCP Target:51823 > Zombie:80 SA id=48658
SENT (1.0800s) TCP Attacker:51987 > Zombie:80 SA id=27659
RCVD (1.2290s) TCP Zombie:80 > Attacker:51987 R id=15679
```

四个伪造的数据包加上来自 Attacker 的探测导致 Zombie 将其 IP ID 从 15674 增加到 15679。完美！现在真正的扫描开始了。请记住，15679 是最新的 Zombie IP ID。

```
Initiating Idlescan against Target
SENT (1.2290s) TCP Zombie:80 > Target:20 S id=13200
SENT (1.2290s) TCP Zombie:80 > Target:21 S id=3737
SENT (1.2290s) TCP Zombie:80 > Target:22 S id=65290
SENT (1.2290s) TCP Zombie:80 > Target:23 S id=10516
SENT (1.4610s) TCP Attacker:52050 > Zombie:80 SA id=33202
RCVD (1.6090s) TCP Zombie:80 > Attacker:52050 R id=15680
```

Nmap 探测端口 20-23。然后它探测 Zombie，发现新的 IP ID 是 15680，仅比之前的值 15679 高 1。在这两个已知数据包之间没有 IP ID 增量，意味着端口 20-23 可能是 `closed|filtered`。也有可能来自 Target 端口的 SYN/ACK 尚未到达。在这种情况下，Zombie 尚未响应 RST，因此其 IP ID 没有递增。为确保准确性，Nmap 稍后将再次尝试这些端口。

```
SENT (1.8510s) TCP Attacker:51986 > Zombie:80 SA id=49278
RCVD (1.9990s) TCP Zombie:80 > Attacker:51986 R id=15681
```

Nmap 再次探测，因为自上次发送探测以来已经过去了 0.4 秒。Zombie（如果不是真正空闲）在此期间可能与其他主机通信，如果在此处未检测到，将导致后续的不准确。幸运的是，这没有发生：下一个 IP ID 如预期为 15681。

```
SENT (2.0000s) TCP Zombie:80 > Target:24 S id=23928
SENT (2.0000s) TCP Zombie:80 > Target:25 S id=50425
SENT (2.0000s) TCP Zombie:80 > Target:110 S id=14207
SENT (2.2300s) TCP Attacker:52026 > Zombie:80 SA id=26941
RCVD (2.3800s) TCP Zombie:80 > Attacker:52026 R id=15684
```

Nmap 探测端口 24、25 和 110，然后查询 Zombie IP ID。它从 15681 跳到 15684。它跳过了 15682 和 15683，意味着这三个端口中有两个可能是开放的。Nmap 无法判断哪两个是开放的，也可能是误报。因此 Nmap 更深入地向下钻取，将扫描分成子组。

```
SENT (2.6210s) TCP Attacker:51867 > Zombie:80 SA id=18869
RCVD (2.7690s) TCP Zombie:80 > Attacker:51867 R id=15685
SENT (2.7690s) TCP Zombie:80 > Target:24 S id=30023
SENT (2.7690s) TCP Zombie:80 > Target:25 S id=47253
SENT (3.0000s) TCP Attacker:51979 > Zombie:80 SA id=12077
RCVD (3.1480s) TCP Zombie:80 > Attacker:51979 R id=15687
```

第一个子组是端口 24 和 25。IP ID 从 15685 跳到 15687，意味着这两个端口中的一个很可能是开放的。Nmap 再次尝试分治法，分别探测每个端口。

```
SENT (3.3910s) TCP Attacker:51826 > Zombie:80 SA id=32515
RCVD (3.5390s) TCP Zombie:80 > Attacker:51826 R id=15688
SENT (3.5390s) TCP Zombie:80 > Target:24 S id=47868
SENT (3.7710s) TCP Attacker:52012 > Zombie:80 SA id=14042
RCVD (3.9190s) TCP Zombie:80 > Attacker:52012 R id=15689
```

端口 24 的探测显示 IP ID 没有跳跃。因此该端口未开放。根据目前的结果，Nmap 初步确定：

- 端口 20-23 为 `closed|filtered`
- 端口 24、25 和 110 中有两个是 `open`
- 端口 24 和 25 中有一个是 `open`
- 端口 24 为 `closed|filtered`

盯着这个谜题足够久，你会发现只有一个解：端口 25 和 110 是开放的，而其他五个是 `closed|filtered`。按照这个逻辑，Nmap 可以停止扫描并立即打印结果。它过去是这样做的，但当僵尸并非真正空闲时，这会产生太多误报的开放端口。因此 Nmap 继续扫描以验证其结果：

```
SENT (4.1600s) TCP Attacker:51858 > Zombie:80 SA id=6225
RCVD (4.3080s) TCP Zombie:80 > Attacker:51858 R id=15690
SENT (4.3080s) TCP Zombie:80 > Target:25 S id=35713
SENT (4.5410s) TCP Attacker:51856 > Zombie:80 SA id=28118
RCVD (4.6890s) TCP Zombie:80 > Attacker:51856 R id=15692
Discovered open port 25/tcp on Target
SENT (4.6900s) TCP Zombie:80 > Target:110 S id=9943
SENT (4.9210s) TCP Attacker:51836 > Zombie:80 SA id=62254
RCVD (5.0690s) TCP Zombie:80 > Attacker:51836 R id=15694
Discovered open port 110/tcp on Target
```

对端口 25 和 110 的探测显示它们如我们之前推断的是 `open`。

```
SENT (5.0690s) TCP Zombie:80 > Target:20 S id=8168
SENT (5.0690s) TCP Zombie:80 > Target:21 S id=36717
SENT (5.0690s) TCP Zombie:80 > Target:22 S id=4063
SENT (5.0690s) TCP Zombie:80 > Target:23 S id=54771
SENT (5.3200s) TCP Attacker:51962 > Zombie:80 SA id=38763
RCVD (5.4690s) TCP Zombie:80 > Attacker:51962 R id=15695
SENT (5.7910s) TCP Attacker:51887 > Zombie:80 SA id=61034
RCVD (5.9390s) TCP Zombie:80 > Attacker:51887 R id=15696
```

为了确保，Nmap 再次尝试端口 20-23。Zombie IP ID 查询显示没有序列跳跃。万一来自 Target 到 Zombie 的 SYN/ACK 来晚了，Nmap 尝试另一次 IP ID 查询。这再次显示没有开放端口。Nmap 现在对其结果足够有信心，可以打印出来。

```
The Idlescan took 5 seconds to scan 7 ports.
Nmap scan report for Target
PORT    STATE           SERVICE
20/tcp  closed|filtered ftp-data
21/tcp  closed|filtered ftp
22/tcp  closed|filtered ssh
23/tcp  closed|filtered telnet
24/tcp  closed|filtered priv-mail
25/tcp  open            smtp
110/tcp open            pop3

Nmap finished: 1 IP address (1 host up) scanned in 5.949 seconds
```

有关 Nmap 空闲扫描实现的完整详细信息，请阅读 Nmap 源代码发行版中的 `idle_scan.cc`。

虽然端口扫描是对可预测 IP ID 序列的巧妙滥用，但它们也可以用于许多其他目的。本书中散布着示例，特别是在第 10 章《检测和破坏防火墙与入侵检测系统》中。