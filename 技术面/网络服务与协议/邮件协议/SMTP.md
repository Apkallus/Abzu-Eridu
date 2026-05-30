## SMTP

概念：
- SMTP 服务器（称为消息传输代理或 MTA）使用 Sendmail 和 Microsoft Exchange 等软件包传输电子邮件。

- 使用内容过滤机制来清洗电子邮件
    1. 入站邮件首先发送给托管安全服务提供商（MSSP）以隔离恶意软件、垃圾邮件和其他威胁
    2. MSSP 将处理后的邮件中继到组织的外部 SMTP 接口（通常是执行进一步过滤的防火墙或设备）
    3. 然后该接口将邮件投递到内部邮件服务器。

整个链路中设备和邮件服务器的可能配置缺陷：
- 网络过滤不足可能允许攻击者与组织的外部 SMTP 接口建立会话并绕过 MSSP。
- 部分服务器无法将电子邮件中继到预期收件人时，发送未送达通知（NDN）消息，从而揭示软件和网络配置细节。

攻击面：
- 直接利用暴露服务中的缺陷（例如利用 Microsoft Exchange 中的已知错误）
- 使用 SMTP 作为传递机制，向更大系统中的易受攻击组件（例如运行内部邮件服务器的防病毒引擎）提供恶意内容

### 服务指纹识别

在准备好邮件服务器和有效域的列表后，对每个 SMTP 端点进行指纹识别，并识别已启用的子系统和功能。邮件服务器软件详细信息可通过横幅抓取、行为分析和被动审查 NDN 获得。

连接时呈现的 SMTP 横幅通常描述实现：
- Nmap 探测
- 若横幅被混淆或未提供足够详细信息，进行手动探测
    - dig 查询 mx 邮件服务器 dns 信息
    - telnet 连接邮件服务器
        - `HELP` 指令查看响应

### 映射 SMTP 架构

如果邮件服务器无法将邮件路由到收件人，它们通常会向源发送详细的 NDN 消息。这给了攻击者推断有效邮箱的机会（这些邮箱稍后会在钓鱼活动中使用）。第二个好处是 NDN 消息包含有用的环境详细信息，包括：

- 主机名和 IP 地址
- 邮件服务器软件版本和配置
- 底层操作系统和服务器配置
- 邮件服务器的物理位置（基于时区和格式）
- 服务器之间的 TLS 配置和支持

RFC 5321 规定 SMTP 标头不得被邮件服务器软件更改。而 SMTP 的 Received 标头揭示有用细节，使用这些材料来映射网络

在测试期间，应该获取每个枚举的域，以及每个暴露的 SMTP 服务，并使用 **Swaks**向不存在的用户发送电子邮件

使用 Swaks 时，请确保使用你可以接收 NDN 消息的电子邮件账户，以及允许你从任意来源发送电子邮件的域（即不使用 SPF）。

#### 识别防病毒和内容检查机制

NDN 消息还可能包含由内容过滤机制（要么是独立的硬件设备，要么是邮件服务器上运行的软件）生成的标头。

通过发送不同内容的消息，你可以使用响应来推测内容过滤策略和防病毒配置。例如，通过在电子邮件中发送 EICAR 测试文件[^2] 来强制识别和警报恶意内容。

[^2]: 参见 https://www.eicar.org/download/eicar.com.txt。

根据收到的 NDN 标头解析 EICAR 测试文件后揭示防病毒引擎。Jon Oberheide 和 Farnam Jahanian 发表的研究扩展了这一策略[^3]。

[^3]: Jon Oberheide and Farnam Jahanian, “Remote Fingerprinting and Exploitation of Mail Server Antivirus Engines”，密歇根大学技术报告 CSE-TR-552-09，密歇根州安娜堡，2009 年 6 月。

#### 已知的防病毒引擎缺陷

在识别出部署的防病毒引擎后，可通过 SMTP 发送恶意内容来利用缺陷。特别是，在 ClamAV、ESET、Kaspersky、Sophos 和 Symantec 引擎中发现了可远程利用的缺陷

### 枚举支持的命令和扩展

可利用的 SMTP 漏洞通常与特定的服务器子系统相关，工具：
- 手动枚举：telnet 连接后 `HELP` 和 `EHLO` 命令进行
- 自动测试：`smtp-commands` 脚本

查询指令与扩展表

查询服务器设备及其 web 应用程序已知缺陷

### 用户账户枚举

Sendmail 和其他服务器允许邮箱和本地用户账户枚举
- `smtp-user-enum` 
- telnet 手动枚举本地用户
    - `EXPN 账户名` 
    - `VRFY 账户名`
    - `RCPT TO:账户名` 



### 暴力密码猜测

使用 `EHLO` 命令识别支持的身份验证机制（本例中为 `LOGIN`、`PLAIN` 和 `CRAM-MD5`），攻击者可以使用这些机制对有效账户执行暴力密码猜测。

工具：
- Hydra
- Nmap `smtp-brute` 脚本

通过网络嗅探使用 `PLAIN`、`LOGIN` 或 `CRAM-MD5` 认证的 SMTP 会话，很容易获得凭据。`DIGEST-MD5`、`GSSAPI` 和 `NTLM` 机制通过相互认证和重放缓解提供攻击保护。

### 绕过内容检查

组织运行内容检查软件以根据给定策略清洗邮件。服务器和客户端软件包以不同方式解析通过电子邮件发送的材料，并且过滤软件和相关组件（即防病毒引擎）中存在缺陷。

存在可利用的条件是因为内容检查系统和客户端软件解析附件 MIME 标头的方式不一致

这种策略类似于通过分片和乱序发送数据包来绕过网络 IPS 时采用的策略——我们修改数据，使其通过安全控制，然后在目的地重新组装。在测试期间，考虑这种策略的变体并识别可利用的条件非常重要。

### 邮件安全特性审查

SMTP 消息很容易被伪造，因此组织使用 SPF、DKIM 和 DMARC 功能来防止各方发送未经授权的电子邮件。

#### SPF

发件人策略框架（SPF - RFC 7208）提供了一种机制，MTA 可以检查为给定域发送电子邮件的主机是否被授权。组织在特殊格式的 TXT DNS 记录中定义域的授权邮件服务器列表。

通过 `dig` 评估 SPF 配置，如示例 9-12 所示。大型组织通常使用 `include` 和 `redirect` 指令，须迭代地逐步检查每个记录以了解配置。

```bash
dig google.com txt | grep spf
dig _spf.google.com txt | grep spf
dig _netblocks.google.com txt | grep spf
dig _netblocks2.google.com txt | grep spf
dig _netblocks3.google.com txt | grep spf
```

#### DKIM

域名密钥识别邮件（DKIM - RFC 6376）是一种机制，通过该机制，出站电子邮件被签名，并由外部 MTA 在通过 DNS 检索域的公钥后进行验证。DKIM 公钥保存在域的 TXT 记录中；但是，你必须同时知道选择器和域名才能检索它。

查看通过 `gmail.com` 的电子邮件的标头，可以检索到 DKIM 签名：

```
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;d=gmail.com;s=20120113; h=mime-version:x-
received:date:message-id:subject:from:to:content-type; bh=fd9JXP6Ngw+hgcG1EbBo7GpsrIIZzdJb9Q/14o
9e5C8=; b=sYlJC2oYWzBUOPIo0jtR4iFsIVqUlwo2QRcG1186hg5ai0oO1nisiOJUD+QXjt
```

`d` 和 `s` 值被组合并输入 `dig`  检索 DKIM 公钥

```bash
dig 20120113._domainkey.gmail.com TXT | grep p=
```

#### DMARC

基于域的消息认证、报告和一致性（DMARC - RFC 7489）是一种扩展 SPF 和 DKIM 的邮件认证方法。策略指示邮件服务器如何处理给定域的电子邮件并报告执行的操作。

DMARC 策略通过 DNS 分发。

**表 9-11. DMARC 策略字段**

| 名称 | 目的 | 示例 |
|------|------|------|
| `v` | 协议版本 | `v=DMARCv1` |
| `p` | 对源自域名的电子邮件的请求处理策略（即 `none`、`quarantine` 或 `reject`） | `p=quarantine` |
| `sp` | 对子域的请求策略 | `sp=reject` |
| `pct` | 将策略应用于一定百分比的消息（用于控制 DMARC 采用并避免意外的报告泛滥） | `pct=20` |
| `ruf` | 取证报告的报告 URI | `ruf=mailto:authfail@example.org` |
| `rua` | 聚合报告的报告 URI | `rua=mailto:aggrep@example.org` |
| `rf` | 定义取证报告格式 | `rf=afrf` |
| `ri` | 定义聚合报告间隔 | `ri=86400` |
| `adkim` | DKIM 对齐模式（`r`（宽松）是默认值，`s` 强制执行严格模式） | `adkim=s` |
| `aspf` | SPF 对齐模式，使用与 DKIM 对齐模式相同的值 | `aspf=r` |

**示例 9-14. 通过 dig 检索 DMARC 策略**

```bash
root@kali:~# dig _dmarc.yahoo.com txt | grep DMARC
_dmarc.yahoo.com.  1785 IN TXT "v=DMARC1\; p=reject\; sp=none\; pct=100\; 
rua=mailto:dmarc-yahoo-rua@yahoo-inc.com, mailto:dmarc_y_rua@yahoo.com\;"
root@kali:~# dig _dmarc.google.com txt | grep DMARC
_dmarc.google.com. 600 IN TXT "v=DMARC1\; p=quarantine\; rua=mailto:mailauth-reports@google.com"
root@kali:~# dig _dmarc.paypal.com txt | grep DMARC
_dmarc.paypal.com. 300 IN TXT "v=DMARC1\; p=reject\; rua=mailto:d@rua.agari.com\; 
ruf=mailto:dk@bounce.paypal.com,mailto:d@ruf.agari.com"
```

PayPal 和 Yahoo 指示邮件服务器拒绝包含无效 DKIM 签名或非源自其网络的消息。然后通知被发送到每个组织内的相应电子邮件地址。Google 以类似方式配置，尽管它指示邮件服务器隔离消息而不是直接拒绝它们。

### 通过 SMTP 进行钓鱼

通过发送精心制作的电子邮件，可以诱骗用户点击超链接、提供凭据和执行代码（例如 JavaScript 和 Microsoft Office 宏）。根据组织的邮件安全功能和配置，你还可以通过外部 SMTP 接口伪造内部电子邮件。

Kali Linux 中的 **The Social-Engineer Toolkit 社会工程工具包（SET）**是一个强大的平台，你可以从中发起钓鱼活动。

#### 侦察

有效的钓鱼活动通过利用对目标环境的了解来欺骗安全意识强的用户。需要关注的重要细节如下：

- 地址格式和命名约定（例如 Smith, Stan `<stan.smith@intel.com>`）
- 组织内使用的客户端软件（例如 Microsoft Outlook）
- 消息详细信息或特点，包括某些用户采用的签名格式
- 识别要克隆的候选 Web 接口

你可以通过获取源自组织的材料（例如包含标头和 HTML 内容的电子邮件）来覆盖上述列表中的前三项。邮件列表存档和 Google 是很好的候选，以及通过向市场或销售部门请求信息来胁迫用户。

如果组织使用多因素认证进行远程访问，你可以通过克隆 SSL VPN Web 端点来捕获凭据并立即将其重放到合法服务来破坏它。

#### 着陆页准备

使用 SET 克隆登录页面并收集凭据。为了获得最佳结果：注册一个用于活动的域，获取有效的 TLS 证书，并使用 `stunnel` 在受害者和 SET 之间代理 HTTPS 流量。

例如，如果克隆的 Web 端点是 `vpn.victim.com`，请考虑获取 `victim-corp.com`，设置 DNS 使 `sslvpn.victim-corp.com` 指向你的 SET 实例，并购买关联的证书，以便用户看到看起来合法的加密连接。

SET 是一个功能强大的实用程序，具有丰富的功能。可以使用它来收集凭据（通过传统的钓鱼攻击）以及利用易受攻击的浏览器插件和组件来获得代码执行

#### 发送电子邮件

SET 中的鱼叉式钓鱼模块使用 Kali Linux 中的 Sendmail MTA 发送电子邮件。然而，为了获得最佳效果，从先前获取的材料中手动制作电子邮件消息（使用与合法电子邮件相同的字体和消息格式），通过 Swaks 将此材料管道传输到本地 Sendmail 服务，然后发送到目标 SMTP 服务器。

在继续之前评估目标的安全状况非常重要。查看 SPF、DKIM 和 DMARC 策略（如果有），并评估暴露的 SMTP 接口的行为，看它们是否会接受来自内部域的材料。如果环境是加固的，你需要设置一个用于发送电子邮件的域（例如 `victim-corp.com`）。

电子邮件的外观和感觉至关重要，语言也很重要，因为你希望用户产生紧迫感以点击恶意链接。

影响钓鱼活动成功的因素包括：

- SMTP 接口不接受来自公共互联网的、从组织内部域发送的电子邮件
- 使用内容过滤在源自组织外部的电子邮件的主题行中添加材料（例如外部或不可信指示符）
- 存在评估目标 URL 信誉的 Web 代理设备
- 使用特定的浏览器或桌面软件客户端

策略：

- 确保活动中使用的 URL 被标记为在线信誉良好
- 确保用于发起活动的邮件服务器看起来也信誉良好
- 通过跟踪会话标识符来衡量活动的有效性
- 利用特权访问（通过 OWA 或 VPN）获取情报
- 占据并分散事件响应团队的注意力

通过侦察、适当的准备（提供域、证书以及信誉良好的 Web 和邮件服务器地址）和集中执行，你很可能会通过钓鱼取得成功。通过准备多个冗余的攻击平台并分散目标安全团队的注意力，你还应该能够实现持久性。