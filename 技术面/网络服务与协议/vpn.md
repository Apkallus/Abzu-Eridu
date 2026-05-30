ip隧道
- ipsec 将ipsec头部+原始ip数据包作为明文ip数据包的载荷
- tls 将原始数据包作为传输层载荷，由应用解包后发送

虚拟网络接口
- tun 网络层，vpn
- tap 链路层，网桥

tun
- 在内核模块 /dev/net/tun 使用 ioctl 传入 ifreq 结构以注册 tun 虚拟接口
- ifconfig或ip命令，设置 tun 接口的ip与网段
- route 设置路由表转发到 tun 接口

vpn
- 来自 tun 接口的数据进行封包，发送到隧道
- 从 socket 接收的数据包进行解包，发送到 tun 接口后，由内核路由
- 使用 select 同时监控 tun 与 socket 接口
- 或需设置 nat 到

工具
- tcpdump 数据包嗅探
- whois 使用自治系统号查询 ip 前缀

# VPN服务

VPN服务通过IPsec、PPTP和TLS为远程用户和分支机构提供访问。服务端点可能被滥用，以获取敏感数据、获得网络访问权限，并通过拒绝服务影响可用性。

## IPsec

IP本质上是一个不安全的协议，缺乏机密性、完整性和认证。正确实现时，IPsec可以抵御以下攻击类型：

*   网络嗅探
*   源伪造（IP欺骗）
*   数据包内数据的修改
*   重放攻击

Internet密钥交换（IKE）[^1]用于认证IPsec对等体并设置VPN参数。建立安全关联（SA），定义发送数据时使用的IPsec协议、加密算法、密钥及其到期时间（也称为生命周期）。

[^1]: 参见 [RFC 2409](https://tools.ietf.org/html/rfc2409)。

### 数据包格式

相互协商的IPsec SA字段定义了对等体之间使用的安全功能。

使用隧道模式IPsec的IP数据报
- 认证头（AH）[^2]通过对IP数据报进行HMAC来提供完整性和数据源认证
- 封装安全载荷（ESP）[^3]封装并加密IP数据报，提供机密性。

[^2]: 参见 [RFC 4302](https://tools.ietf.org/html/rfc4302)。
[^3]: 参见 [RFC 4303](https://tools.ietf.org/html/rfc4303)。

### ISAKMP、IKE和IKEv2

Internet安全关联和密钥管理协议（ISAKMP）服务支持IKE，并通过UDP端口500暴露。

IKE涉及定义IPsec SA的两阶段过程：
- 第一阶段认证对等体并建立ISAKMP SA（用于保护第二阶段消息）
- 第二阶段建立IPsec SA（用于加密数据）
- 在某些实现中，一种称为XAUTH的机制引入了一个额外的阶段来支持用户认证。

IKEv2标准[^4]解决了IKE中可利用的缺陷，将两个阶段压缩为一组消息。

[^4]: 参见 [RFC 7296](https://tools.ietf.org/html/rfc7296)。

### IKE评估

`ike-scan`工具[^5]

[^5]: 参见GitHub上的 [ike-scan](https://github.com/royhills/ike-scan)。

这种技术可以识别大多数IPsec服务器，但如果IKE服务仅接受来自特定地址的请求或期望特定的转换集，则可能会失败。IKE转换集定义了密钥交换期间使用的加密算法、完整性算法、认证模式和Diffie-Hellman（DH）组。识别到可访问的IKE服务后，您可以使用ike-scan进一步探测它们，以了解其配置和潜在弱点。

#### IKE服务指纹识别

ike-scan工具通过分析供应商ID值和IKE退避模式来识别IPsec实现。使用`-M`标志将输出拆分为多行，使用`-o`显示实现猜测。

如果没有返回响应，则可能需要特定的转换字段。

#### 支持的转换枚举

使用自定义转换属性 `-a` 运行 ike-scan，可推测工程配置并识别弱点（例如，有缺陷的加密算法和认证方法）。IKE转换字段及常见值如下：

*   **加密算法**
    1（DES），5（3DES），7/128（AES-128），7/256（AES-256）
*   **完整性算法**
    1（MD5），2（SHA-1），4（SHA-256），5（SHA-384），6（SHA-512）
*   **认证方法**
    1（PSK），3（RSA），65001（XAUTH）
*   **DH组**
    1（768位），2（1024位），5（1536位），14（2048位），15（3072位）

### 可利用的IPsec弱点

IPsec实现容易受到以下攻击：

*   如果使用弱DH组，数据可被被动解密
*   利用漏洞（例如，远程代码执行）产生意外影响
*   主动和被动枚举激进模式身份[^6]
*   暴露并破解预共享密钥（PSK）值
*   一旦知道PSK，获取XAUTH凭证

[^6]: 参见瞻博网络的 [“IPSec VPN Username Enumeration Vulnerability”](http://juni.pr/2aAs0Hw)。

IKE和IKEv2都使用DH进行密钥交换。生成具有特殊属性的质数计算负担很重，因此IPsec对等体支持固定的标准化参数，称为组。这些“安全”参数于1998年发布，并被其他应用程序使用，包括SSH、Tor和OTR。

Cisco特别建议避免使用DH组1和2[^7]，这源于一篇研究论文[^8]。该论文的作者描述了国家行为者如何可能通过离散对数预计算，解密使用弱组协商的IPsec会话。花费数亿美元进行预计算，可以通过实时解密任何使用弱组（1024位或更小）的会话来实现成本摊销。

[^7]: 参见Cisco.com上的 [“Next Generation Encryption”](http://bit.ly/2aQr7uP)。
[^8]: Adrian David等人，[“Imperfect Forward Secrecy: How Diffie-Hellman Fails in Practice”](http://bit.ly/2aCKJPZ)，第22届ACM SIGSAC计算机与通信安全会议论文集，科罗拉多州丹佛，2015年10月12-16日。

### 激进模式IKE组枚举

许多IPsec实现支持激进模式IKE和PSK认证。

工具：
- 手动：ike-scan 根据服务器响应枚举有效的身份（称为组）
- 自动：`ikeforce.py`[^11]，该工具还会测试 Cisco ASA 激进模式IKE组枚举缺陷。

[^11]: 参见GitHub上的 [ikeforce.py](http://bit.ly/2ax0rev)。

组值也可以通过网络嗅探获得，因为在激进模式IKE交换期间，详细信息以明文形式发送。
- 使用tcpdump被动获取发起者的身份。

组可以是电子邮件地址、用户名或任意标签。

### 激进模式IKE PSK破解

使用ike-scan从支持激进模式的端点获取PSK哈希。通常需要一个有效的组（通过`-n`参数提供）。使用`psk-crack`破解哈希

在Trustwave SpiderLabs博客[^12]中找到关于此漏洞的进一步讨论。

[^12]: Daniel Turner, [“Cracking IKE Mission: Improbable (Part 1)”](http://bit.ly/2b5At3v), Trustwave SpiderLabs Blog, 2013年3月27日。

### 攻击XAUTH

大多数实现使用激进模式IKE和PSK进行组认证，并使用XAUTH提供额外的用户认证（通过Microsoft Active Directory、RADIUS等）。在IKEv2中，EAP取代XAUTH来认证用户。

支持XAUTH的IPsec服务器在被探测时会返回一个特定的VID值。使用 ike-scan 枚举XAUTH支持

XAUTH机制依赖于PSK（组密钥）的强度，使其容易受到中间人攻击[^13]和暴力破解密码的威胁。掌握了有效的组名和密钥后，您可以执行以下操作：

[^13]: John Pliam, [“Authentication Vulnerabilities in IKE and Xauth with Weak Pre-Shared Secrets”](http://bit.ly/2b5ALri), 1999年10月2日。

*   通过使用`fiked`[^14]建立一个伪造的IKE服务并收集用户凭证
*   使用`ikeforce.py`[^15]暴力破解XAUTH用户密码

[^14]: Daniel Roethlisberger, [“FakeIKEd”](https://www.roe.ch/FakeIKEd), Rö’s Wiki, 2012年5月13日。
[^15]: Dan Turner, [“IKEForce Brute”](https://vimeo.com/106615524), Vimeo视频, 发布于2014年9月19日。

### 使用IPsec VPN进行认证

Kali Linux中的`vpnc`用于建立经过认证的IPsec隧道。配置文件位于`/etc/vpnc/`下，并通过命令行使用`vpnc`调用。

## PPTP

点对点隧道协议（PPTP）[^16]通常用于为移动设备提供远程访问，它使用TCP端口1723进行密钥交换，并使用IP协议47（GRE）[^17]在对等体之间加密数据。由于协议复杂性和对MS-CHAP认证的依赖，PPTP容易受到攻击，正如Bruce Schneier[^18]所描述，并被Moxie Marlinspike的`chapcrack`[^19]所利用。

[^16]: 参见 [RFC 2637](https://tools.ietf.org/html/rfc7296)。
[^17]: 参见 [RFC 2784](https://tools.ietf.org/html/rfc2784)。
[^18]: Bruce Schneier, [“Analysis of Microsoft PPTP Version 2”](http://bit.ly/2aocT0p), Schneier on Security。
[^19]: 参见GitHub上的 [chapcrack](https://github.com/moxie0/chapcrack)。

指纹识别：
- Nmap，在可用时显示主机名、供应商和固件信息。

暴力破解密码
- `thc-pptp-bruter` 工具
    使用`-n`和`-l`选项调整并行尝试次数。

## VPN测试总结

测试IPsec和PPTP服务的策略包括：

**服务指纹识别和软件评估**
对可用服务进行指纹识别，以识别导致意外后果（例如信息泄露、代码执行或拒绝服务）的软件缺陷。IPsec和PPTP服务都可能泄露在其他地方有用的主机名和固件详细信息。

**识别加密弱点**
DH组1和组2容易受到攻击；然而，利用需要网络访问以获取密钥交换消息和密文。如果使用MD5或SHA-1进行完整性检查，也可能导致材料被伪造而产生意外后果。

**利用激进模式IKE**
对激进模式的支持可以被动和主动地利用，以获取有效的组和PSK值，进而损害XAUTH凭证（如果使用），这些凭证可用于获得认证访问。

**暴力破解密码**
弱PPTP和XAUTH用户密码很容易通过暴力破解获得。在许多环境中，对VPN认证日志的审查是事后才考虑的事情，因此这个向量特别有用。

## VPN服务对抗措施

在加固VPN服务时，应考虑以下对抗措施：

*   确保VPN服务器保持更新并打上补丁，以减轻影响机密性、完整性和可用性（所有这些对VPN操作都至关重要）的攻击。
*   禁用对弱认证方法和加密算法的支持。不要依赖客户端偏好或设置。特别是，应禁用激进模式IKE、DES加密、MD5和SHA-1完整性检查，并强制执行AH和ESP功能（提供认证和机密性）。
*   优先使用IKEv2，并至少强制执行DH组14（2048位）以实现安全的密钥交换。IKE和小DH组容易受到攻击，导致加密数据被破坏。
*   使用数字证书来消除对预共享密钥的依赖，并提供设备认证。Microsoft Active Directory证书服务尤其支持计算机证书的提供。
*   对用户帐户强制执行多因素认证（MFA），并考虑第三方平台，如Duo Security和Okta。一次性密码（OTP）机制在内部也很容易设置（例如，OpenVPN Access Server和Google Authenticator[^20]）。
*   过滤入站VPN流量，以在发生入侵时限制网络访问。考虑在网络中使用堡垒主机和其他阻塞点，以提供纵深防御。
*   审计和审查VPN认证成功和失败事件，以识别密码暴力破解活动和受损的用户凭证（例如，从不同地理位置登录）。
*   定期审计授权的VPN用户，以识别流氓帐户。攻击者在破坏Active Directory、RADIUS、LDAP和其他认证提供商后，会在大规模环境中通过添加新帐户来持续存在。

[^20]: 参见OpenVPN.net上的 [“Google Authenticator Two-Step Authentication”](http://bit.ly/2a2GsEW)。