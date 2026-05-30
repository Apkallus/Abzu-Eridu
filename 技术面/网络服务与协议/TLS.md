概念
- tls 位于应用层，将应用层或传输层数据加密、解密、完整性检查后传输
- 拥有多种协议，其中握手协议用来建立安全通道，应用协议用来传输数据



密钥生成
- 预主秘钥，客户端产生随机数后使用服务器公钥加密
- 主密钥，使用预主秘钥与前两步交换的随机数生成
- 会话密钥，分为4部分，客户端与服务器分别获得其 mac 与加密 key

数据传输
- SSL_write 函数
	- 将数据分块
	- 对每个块计算mac
	- 添加填充
	- 加密后放入tsl头部后的载荷段
- SSL_read 函数
	- 解密
	- 验证mac
	- 缓存：从tcp中取出，但尚未被应用程序使用的数据块暂存在tls缓存。若不足，则持续从tcp缓存取出直到空

tls编程
- 建立tls上下文
	- 客户端
		- 检查服务器公钥证书
		- 启用主机名检查，回调函数为空时默认在不匹配时终止，若设置回调函数需使用返回值设置是否终止
	- 服务器
		- 不要求客户端提供公钥证书
		- 加载服务器证书，以提供到客户端
		- 加载服务器私钥，以解密客户端发送的使用服务器公钥加密的信息
- 建立tcp连接
- 绑定tls到tcp连接，进行tls握手
- 使用加密的tls会话

# 第11章 评估TLS服务

互联网工程任务组（IETF），将Netscape SSL 3.0协议转化为标准——官方名称为传输层安全（TLS），并于1999年由RFC 2246批准。

Ivan Ristić的《Bulletproof SSL and TLS》（Feisty Duck, 2014）整个书籍都致力于这个主题，提供了关于TLS及其特性的更多细节。[^1]

图11-1显示了TLS运行在OSI第6层，为上层应用协议（此处为HTTP）提供传输安全。本章描述了TLS 1.2版本[^2]的机制，以及应对TLS和传统SSL端点采取的评估策略。SSL 3.0尤其存在缺陷，在线支持正在迅速淘汰。

[^1]: 您还可以查看 [Ivan Ristić的博客](https://blog.ivanristic.com)。
[^2]: 参见 [RFC 5246](https://tools.ietf.org/html/rfc5246)。

TLS依赖TCP作为底层传输协议。DTLS[^3]是一个较少为人知的协议，可以运行在第4层数据报协议之上，包括UDP、DCCP[^4]和SCTP。包括Google Chrome和Mozilla Firefox在内的Web浏览器都支持DTLS。

[^3]: 参见 [RFC 4347](https://tools.ietf.org/html/rfc4347)。
[^4]: 参见 [RFC 5238](https://tools.ietf.org/html/rfc5238)。

## TLS机制

对等体之间通过记录发送数据。查看 TLS 记录的格式。

### 会话协商

TLS会话通过握手记录建立，用于执行以下操作：

*   商定协议和密码套件
*   商定压缩方法和扩展
*   传输随机数（称为nonce）
*   传输X.509数字证书和加密密钥
*   验证彼此证书的所有权

认证发生并生成主密钥。对等体发送Change Cipher Spec记录，指示对方从现在开始发送的材料将被加密和签名，同时发送一个Finished消息，其中包含先前消息的HMAC。在验证每个Finished消息的内容后，会话建立，数据通过Application记录发送

tls握手
- 概念：设置加密参数并生成会话秘钥
- 步骤
	- 客户端发送
		- 支持的加密方式集合
		- 客户端随机数
	- 服务器发送
		- 从客户端发送的加密集合中选择的加密方式
		- 服务器端随机数
		- 公钥证书
		- 握手结束消息
	- 客户端发送
		- 秘钥交换消息，生成预主秘钥并使用服务器公钥加密
		- 更改密码规范的消息
		- 加密完成消息，并包含hash与mac进行最终验证
	- 双方使用 预主秘钥 -› 主秘钥 -› 会话秘钥
		
	- 服务器端发送
		- 更改密码规范的消息
		- 加密完成消息，并包含hash与mac进行最终验证

#### Client Hello

客户端发送的第一条消息包含以下字段：

*   客户端希望使用的TLS版本（即支持的最高版本）
*   一个256位随机数
*   客户端为此连接使用的会话ID值（如果有）
*   首选密码套件列表（按偏好顺序排列）
*   可选的首选TLS压缩方法列表[^5]
*   传达客户端能力给服务器的TLS扩展数据[^6]

[^5]: 参见 [RFC 3749](https://tools.ietf.org/html/rfc3749)。
[^6]: 参见IANA.org上的 [“Transport Layer Security (TLS) Extensions”](http://bit.ly/2aQqC40)。

两个特别重要的字段是TLS版本和密码套件列表。压缩功能计划在TLS 1.3中移除，扩展包括对椭圆曲线密码学（ECC）和安全重新协商的支持。

#### Server Hello

收到Client Hello消息后，服务器响应以下内容：

*   服务器希望使用的TLS版本
*   一个256位随机数
*   服务器希望使用的会话ID值（如果有）
*   为会话选择的密码套件
*   选择的压缩方法
*   TLS扩展数据

此时，对等体已就密钥交换和认证算法、要使用的附加功能达成一致，并共享了它们的随机值。如果选择了经过认证的密钥交换机制，则随后共享证书和附加材料。

#### 服务器证书与密钥交换

服务器使用Certificate消息传输其证书。在某些情况下（例如，使用临时密钥的Diffie-Hellman），证书不包含密钥材料，而是使用Server Key Exchange消息发送参数。

如果服务器想要认证客户端，还会发送Certificate Request消息。相互认证引入了一个有用的安全层（防止未经授权访问运行在TLS之上的服务），尽管大多数系统不以这种方式运行。

然后服务器发送Server Hello Done消息，表示它已完成消息发送，正在等待客户端的响应。

#### 客户端证书与密钥交换

如果服务器请求，客户端通过Client Certificate消息发送其证书。接下来使用Client Key Exchange消息，通过以下三种格式之一将密钥发送给服务器：

**RSA**
客户端使用服务器的公钥加密预主密钥后发送。双方独立计算主密钥和密钥块（使用256位随机值和384位预主密钥）。如果服务器能够解密此消息并生成有效的密钥块，则客户端已证明其真实性。

**Diffie-Hellman (DH)**
客户端发送其DH公值并计算预主密钥。

**椭圆曲线Diffie-Hellman (ECDH)**
客户端发送其ECDH公值（可选择使用DSA或RSA签名）。

如果客户端先前发送了Client Certificate消息（执行相互认证），则Certificate Verify消息通过使用其私钥生成到当前为止消息的HMAC来对客户端进行认证。

#### Finished

客户端发送Change Cipher Spec记录，通知服务器之后的所有数据都将被加密。客户端还发送一个Finished消息，其中包含会话的HMAC。服务器执行相同的操作——发送Change Cipher Spec记录指示客户端从现在开始材料将被加密，以及一个包含交换HMAC的Finished消息。客户端和服务器在验证HMAC值后，确保会话的完整性并相互认证。

### 密码套件

TLS 1.2密码套件条目定义以下参数：

*   密钥交换和认证方法
*   批量对称加密算法、密钥长度和模式
*   消息认证码（MAC）算法和PRF

RFC 5246列出了TLS 1.2的36个基本密码套件。RFC 4492引入了另外25个ECC套件，这些套件被包括Google Chrome在内的许多Web浏览器所青睐。[^7]为了演示密码套件的格式和布局，以下为两个示例：

`TLS_RSA_WITH_RC4_128_MD5`
RSA同时用于密钥交换和认证。认证后，对等体使用128位RC4加密数据，并使用128位HMAC-MD5确保完整性。

`TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA`
ECDHE结合椭圆曲线数字签名算法（ECDSA）进行认证。认证后，对等体使用密码块链接模式下的256位AES（AES_256_CBC）加密数据，并使用160位HMAC-SHA1确保完整性。

[^7]: 参见IANA.org上的 [“Transport Layer Security (TLS) Parameters”](http://bit.ly/2aVB1wR)。

`openssl ciphers -v`列出OpenSSL支持的密码
- Kx值定义密钥交换算法
- Au表示认证机制
- Enc定义批量对称加密算法和密钥长度
- Mac定义用于完整性检查的HMAC函数


用于完整性检查的AEAD值[^8]。GCM密码（例如AES256-GCM）同时提供加密和完整性保护，因此该值设置为AEAD（相对于SHA-1、SHA-256或SHA-384）。该算法也成为用于生成主密钥的伪随机函数（PRF）。

[^8]: 参见维基百科上的 [“Authenticated encryption”](http://bit.ly/2aVAT0h)。

### 密钥交换与认证

TLS支持多种密钥交换和认证机制，对等体之间发送的值用于生成预主密钥、主密钥和密钥块。流行的机制有：

*   RSA密钥交换和认证
*   DH静态密钥交换，使用RSA或DSA认证
*   临时DH密钥交换，使用RSA或DSA认证
*   DH或DHE的ECC版本，使用RSA、DSA或ECDSA认证

OpenSSL等支持的不太常见的算法包括SRP[^9]和PSK[^10]。

[^9]: 参见 RFC [2945](https://tools.ietf.org/html/rfc2945) 和 [5054](https://tools.ietf.org/html/rfc5054)。
[^10]: 参见维基百科上的 [“TLS-PSK”](http://bit.ly/2aLlJrJ)。

#### RSA密钥交换与认证

在协商期间，客户端和服务器相互发送256位随机值。前32位应基于本地系统时间，其余224位应使用PRNG生成。

预主密钥:
	客户端生成一个额外的368位随机数，并将其附加到会话的TLS版本（先前在Client Hello消息中发送）的16位值上。

预主密钥使用服务器的RSA公钥加密，并通过Client Key Exchange消息发送。使用服务器的公钥意味着这种密钥交换方法不提供前向保密性[^11]。然而，由于明文值规定了先前指定的TLS协议版本，因此可以防止回滚和带内降级攻击。

[^11]: Vincent Bernat, [“SSL Computational DoS Mitigation”](http://bit.ly/2aAtPUC), MTU Ninja Blog, 2011年11月1日。

**生成主密钥和密钥块。** 客户端和服务器使用相同的PRF生成主密钥和密钥块。TLS 1.2中的PRF可通过密码套件协商，默认为SHA-256。较旧版本的TLS和SSL使用MD5和SHA-1。

主密钥长度始终为384位。然而，根据PRF和密码套件的不同，密钥块的大小可能不同。例如，AES_256_CBC_SHA256需要1024位的块，该块被分成三个密钥对：

*   两个256位MAC密钥
*   两个256位加密密钥
*   两个256位初始化向量（IV）值

客户端和服务器使用这些密钥来加密、解密、签名和验证数据。

#### DH密钥交换

DH密钥交换允许两方通过公共信道建立秘密（此处为预主密钥）。使用RSA的密钥交换则不同，因为预主密钥由客户端生成并发送给服务器（使用服务器的公钥加密）。DH是一种匿名密钥协商协议，因此使用RSA和DSA提供认证。TLS 1.2定义了五种基本操作模式

| 密码套件         | 密钥类型        | 传输方式                                           |
|-----------------|----------------|----------------------------------------------------|
| DH_RSA          | 静态            | 服务器证书（RSA签名）                              |
| DH_DSS          | 静态            | 服务器证书（DSA签名）                              |
| DHE_RSA         | 临时            | Server Key Exchange消息（RSA签名）                 |
| DHE_DSS         | 临时            | Server Key Exchange消息（DSA签名）                 |
| DH_anon         | 匿名            | Server Key Exchange消息（未签名）                  |

数字签名算法（DSA）是NIST在FIPS 186-4中发布的数字签名标准（DSS）的一部分。大多数文档提到DSA；然而，有些使用DSS来表示该机制。

DH公钥（称为参数）通过Certificate和Server Key Exchange消息从服务器发送到客户端。静态参数位于服务器证书中，并从服务器的私钥派生。临时参数为每个TLS会话生成，并提供前向保密性。

对等体执行以下操作以生成预主密钥：

1.  服务器向客户端发送DH域参数（`dh_g`和`dh_p`），如果使用认证模式，这些参数会被签名。`dh_p`值应该是一个大的质数，`dh_g`值应该是一个小的本原根（也称为生成元）。
2.  客户端生成一个私有随机数（`rand_c`）并执行以下操作，将`dh_g`值提高到`rand_c`次幂，并对`dh_p`取模[^12]以计算`dh_Yc`：

    `dh_g^rand_c mod dh_p = dh_Yc`

3.  服务器生成自己的私有随机数（`rand_s`）并执行相同操作以计算`dh_Ys`：

    `dh_g^rand_s mod dh_p = dh_Ys`

4.  `dh_Yc`和`dh_Ys`公值被公开通信。
5.  客户端使用`dh_Ys`和`rand_c`计算预主密钥：

    `dh_Ys^rand_c mod dh_p = secret`

6.  服务器使用`dh_Yc`和`rand_s`执行相同操作：

    `dh_Yc^rand_s mod dh_p = secret`

[^12]: 参见维基百科上的 [“Modular arithmetic”](http://bit.ly/2awjZBx)。

在静态模式下使用DH时，`dh_g`、`dh_p`、`dh_Ys`和`rand_s`是固定的，不提供前向保密性。

双方之间的预主密钥是一致的，因为步骤2和3的总和值使用各方的私有随机数再次求幂，结果得到相同的总和。只要`dh_p`足够长（超过1024位），进行暴力破解以获取秘密的成本高得令人望而却步。

计算预主密钥后，每一方生成一个主密钥和密钥块（如图11-4和图11-5所示）。

回顾一下，基本的数学演示如下：

1.  服务器选择一个`dh_g`值（3）和一个`dh_p`值（17），并发送给客户端。
2.  客户端选择一个`rand_c`值15并生成`dh_Yc`：

    `3^15 mod 17 = 6`

3.  服务器选择一个`rand_s`值13并生成`dh_Ys`：

    `3^13 mod 17 = 12`

4.  公值`dh_Yc`和`dh_Ys`（6和12）被分发。
5.  客户端执行：

    `12^15 mod 17 = 10`

6.  服务器执行：

    `10^13 mod 17 = 10`

**DH参数选择与协商。** 服务器单方面定义会话的域参数，因此可以向客户端提供弱值。例如，`dh_p`应该是一个大的质数，但许多客户端接受小的质数（甚至不是质数的值），导致会话安全性较弱。还可以发起跨协议攻击，向客户端提供已签名的ECDH参数，这些参数被误解为普通DH参数。[^13]

[^13]: Nikos Mavrogiannopoulos等人, [“A Cross-Protocol Attack on the TLS Protocol”](http://bit.ly/2aFHUh9), 2012年ACM计算机与通信安全会议论文集，北卡罗来纳州罗利，2012年8月16-18日。

TLS 1.3计划移除对自定义DH参数组的支持。

### ECC

DH和DSA的ECC版本由RFC 4492定义。ECC因其使用较小的私钥大小且速度快而具有吸引力。

| 密码套件         | 密钥类型        | 传输方式                                           |
|-----------------|----------------|----------------------------------------------------|
| ECDH_ECDSA      | 静态            | 服务器证书（ECDSA签名）                            |
| ECDH_RSA        | 静态            | 服务器证书（RSA签名）                              |
| ECDHE_ECDSA     | 临时            | Server Key Exchange消息（ECDSA签名）               |
| ECDHE_RSA       | 临时            | Server Key Exchange消息（RSA签名）                 |
| ECDH_anon       | 匿名            | Server Key Exchange消息（未签名）                  |

服务器在握手期间定义命名曲线，引用已发布的曲线和参数集。有了参数，每一方使用私钥产生一个公值，该公值被通信并用于独立生成预主密钥。有些曲线是不安全的，应该避免，如Daniel J. Bernstein和Tanja Lange的SafeCurves项目[^14]所述。

[^14]: Daniel J. Bernstein and Tanja Lange, [“SafeCurves: Choosing Safe Curves for Elliptic-Curve Cryptography”](http://safecurves.cr.yp.to), 2014年12月1日。

### TLS认证

包括TLS在内的系统使用X.509证书来认证客户端、服务器和用户。操作系统和Web浏览器包含可信证书颁发机构（CA）的公钥，这些公钥用于签名单个证书。

#### X.509格式

这些属性传达证书有效性、实体身份（即主机或用户名）以及相关的公钥。签名算法和签名值扩展用于由给定机构（称为颁发者）对证书进行签名。

**X.509证书字段**

| 字段                    | 描述                                                       |
|-------------------------|------------------------------------------------------------|
| 版本 (Version)          | 定义X.509版本                                              |
| 序列号 (Serial number)  | 给定颁发者为每个证书分配的唯一标识符                       |
| 签名 (Signature)        | 用于签署证书的算法                                         |
| 颁发者 (Issuer)         | 标识签署证书的实体                                         |
| 有效期 (Validity)       | 定义证书的有效期                                           |
| 主体 (Subject)          | 标识与公钥关联的实体                                       |
| 主体公钥信息 (Subject public key) | 描述主体的公钥和相应算法（即RSA、DSA或DH）               |
| 唯一标识符 (Unique identifiers) | 颁发者和主体标识符                                         |
| 扩展 (Extensions)       | 允许设置特定策略和传达数据的扩展（例如，使用的签名算法和CA公钥值） |

在测试期间，使用OpenSSL命令行工具的`s_client`[^15]和`x509`模式来检索和处理X.509证书。输出显示证书字段和扩展。

[^15]: 参见 [OpenSSL s_client 文档](http://bit.ly/2aTuFh6)。


#### CA与证书链

TLS对等体通常通过验证X.509证书中的颁发者和签名值来相互认证。CA使用其私钥签名证书，相应的公钥作为受信任的根证书分布在操作系统和浏览器中。

在X.509中，CA标志用于指定证书是否可以用于签署其他证书（`CA:true`）或不可以（`CA:false`）。证书链通过使用此标志形成——根CA签署下级CA（称为中间CA）的证书，这些下级CA又可以签署其他证书。

存在许多根CA和中间CA。EFF在其中确定了超过650个可以签署X.509证书的组织，这些证书受到Microsoft和Mozilla的信任。[^16]

[^16]: 参见电子前沿基金会的 [“The EFF SSL Observatory”](https://www.eff.org/observatory)。


#### 密钥生成与处理

RSA密钥对生成。随机选择两个大质数，将其输入RSA算法以计算私钥和公钥。公值放在X.509证书中，然后由CA签名。

私钥和用于生成它的材料（即随机质数）必须以安全的方式生成和处理。例如，2008年Debian Linux中的PRNG缺陷导致使用OpenSSL生成的私钥可预测。[^17][^18]

[^17]: Bruce Schneier, [“Random Number Bug in Debian Linux”](http://bit.ly/2aXzeEw), Schneier on Security, 2008年5月19日。
[^18]: 参见 [CVE-2008-0166](http://bit.ly/2bcmJHn)。

私钥不应留在用户主目录、版本控制系统（例如GitHub）中，也不应通过全局可读权限暴露。

#### 签名算法缺陷

Microsoft、Google和其他组织正在逐步淘汰SHA-1，而MD5已经完全被破解（如Flame恶意软件所利用）。

**表11-4. X.509签名算法**

| 哈希函数     | 签名使用           | 备注                                   |
|--------------|--------------------|----------------------------------------|
| MD5          | RSA                | 已被破解，易于利用[^a]                 |
| SHA-1        | RSA、DSA或ECDSA    | 弱，但尚无已知碰撞                     |
| SHA-256      | RSA、DSA或ECDSA    | 在撰写本文时实际安全                   |
| SHA-384      | RSA、DSA或ECDSA    |                                        |
| SHA-512      | RSA、DSA或ECDSA    |                                        |

[^a]: Nat McHugh, [“How I Created Two Images with the Same MD5 Hash”](http://bit.ly/2aNK2q5), Nat McHugh Blog, 2014年10月31日。

### 会话恢复

通过进行完整握手来恢复TLS会话的计算成本很高。因此，服务器支持消除完整往返的恢复模式：

**TLS恢复**
如果对等体先前协商过主密钥，则可以使用简化的握手来恢复TLS会话。Client Hello包含一个会话ID，如果服务器识别该ID并具有相应的主密钥，则可以使用。由于随机值是新的，因此会生成一个新的密钥块。

**TLS会话票据扩展**
在大型环境中，服务器端维护状态存在挑战，因此一种由客户端存储会话标识符（使用服务器的私钥加密）的机制被批准为TLS扩展。[^23]恢复机制与以前相同，但客户端维护状态。在实践中，在负载均衡的TLS端点之间部署该扩展需要仔细考虑：所有服务器必须使用共享私钥初始化，并且可能需要额外的机制来定期轮换它。

[^23]: 参见 [RFC 5077](https://tools.ietf.org/html/rfc5077)。

### 会话重新协商

TLS会话可以在现有安全通道上进行重新协商，以重新生成密钥或执行进一步的认证。该机制中发现了一个缺陷[^24]，通过该缺陷，具有网络访问权限的攻击者可以拦截并持有来自合法客户端的握手记录，自己与服务器建立TLS会话，发送应用数据，发起重新协商，并释放合法的握手记录。由于重新协商是在现有通道上执行的，服务器认为会话是同一个。然后来自客户端和攻击者的数据都被接受。

[^24]: 参见 [CVE-2009-3555](http://bit.ly/2bco9S4)。

Thierry Zoller发表了一篇描述此问题和实际攻击向量的论文。[^25]总之，他指出了导致任意HTTP请求注入、从HTTPS降级到HTTP以及通过TRACE方法向客户端呈现恶意内容的缺陷。

[^25]: Thierry Zoller, [“TLS/SSLv3 Renegotiation Vulnerability Explained”](http://bit.ly/2ay5Ghl), SlideShare.net, 2013年2月6日。

引入了一个TLS扩展，通过加密方式将重新协商与现有会话绑定来解决该问题。[^26]此后，流行的TLS库已经实现了该扩展并支持安全重新协商。

[^26]: 参见 [RFC 5746](https://tools.ietf.org/html/rfc5746)。

### 压缩

TLS 1.2及更早版本通过DEFLATE[^27]支持压缩。当压缩应用于包含HTTP头（具有已知结构和格式）的块时，可以通过观察压缩后的密文来揭示会话令牌。CRIME攻击针对TLS本身的压缩，而BREACH和TIME攻击则利用HTTP压缩（无论传输层如何）来揭示HTTP响应中的秘密。

[^27]: 参见 [RFC 1951](https://tools.ietf.org/html/rfc1951)。

### STARTTLS

STARTTLS命令用于在明文协议（例如SMTP、IMAP、POP3或FTP）上建立TLS会话，如示例11-4通过SMTP[^28]所示。在确认STARTTLS指令后协商TLS会话，涉及如前所述的记录交换。

[^28]: 参见 [RFC 3207](https://tools.ietf.org/html/rfc3207)。

通过明文和加密服务通道支持的功能通常存在差异。例如，认证机制可能不同（或通过明文会话不存在），这可以通过暴力破解密码进行攻击。

## 理解TLS漏洞

攻击者可以远程利用某些TLS缺陷（例如，实现中的内存损坏），但对许多缺陷的实际利用需要网络访问权限以破坏密文并注入应用数据。

自2011年以来，Juliano Rizzo、Thai Duong等人已经发现了SSL和TLS中的许多缺陷，包括BEAST、CRIME、BREACH和POODLE等名称。利用这些漏洞通常需要以下条件：

*   受害者浏览器执行恶意代理（例如JavaScript）
*   网络访问以监控受害者生成的密文
*   与代理的通信通道以修改明文

在撰写本文时，有两个值得注意的例外：

*   对TLS服务器实现中的时序侧信道（例如，后面讨论的Lucky 13）的实际利用通常需要网络邻近或对TLS服务器的低延迟访问，以便收集准确的度量数据。
*   如果不需要捕获密文（例如TIME），攻击可以远程发起。

### 可利用的缺陷

影响SSL和TLS的缺陷分为两类：

*   协议弱点（例如SSL 3.0、TLS 1.0或HTTP压缩）
*   特定实现中的漏洞（例如OpenSSL 1.0.1g）

包含旧协议（包括SSL 3.0和TLS 1.0）中的重大漏洞，以及严重的实现缺陷（例如OpenSSL heartbleed漏洞）。


### 缓解TLS风险

表11-6列出了针对所讨论的TLS漏洞的缓解步骤。许多问题（包括CRIME、BREACH和POODLE）也已在Google Chrome和Mozilla Firefox中得到缓解。

**表11-6. TLS攻击缓解策略**

| 攻击                      | 缓解措施                                                                 |
|---------------------------|--------------------------------------------------------------------------|
| Logjam                    | 强制DH组大小为1024位及以上                                                |
| POODLE                    | 禁用对SSL 3.0的支持                                                      |
| BEAST                     | 强制使用TLS 1.1及更高版本                                                 |
| CRIME                     | 禁用TLS压缩                                                              |
| BREACH和TIME              | 禁用HTTP压缩                                                             |
| Lucky 13                  | 如果服务器实现有缺陷，禁用CBC密码                                        |
| RC4字节偏差               | 禁用对RC4密码套件的支持                                                  |
| FREAK                     | 禁用对弱出口级密码的支持                                                  |
| 不安全的重新协商          | 升级服务器和客户端软件到最新版本                                          |
| 不安全的回退              |                                                                          |
| DH参数篡改                |                                                                          |
| 实现缺陷                  |                                                                          |

#### 在Web应用程序中缓解Lucky 13和RC4字节偏差

已发布的针对TLS的攻击往往侧重于凭证暴露（例如，从客户端发送到服务器的HTTP会话令牌和密码）。攻击实际上依赖于在客户端浏览器中运行的JavaScript代理，通过TLS生成请求。

对于Lucky 13和RC4字节偏差攻击，HTTP头（包括会话令牌）会多次发送到服务器。包括POODLE和BEAST在内的攻击使用选择边界[^37]并逐字节计算明文值，这需要的流量少得多。

[^37]: Erland Oftedal, [“The Chosen-Boundary Attack”](http://bit.ly/2aQtBt6), Insomnia and the Hole in the Universe Blog.

Lucky 13攻击使用大约524,000（2^19）个连接来恢复base64编码的会话令牌，而RC4字节偏差攻击需要超过1670万（2^24）个连接来恢复特定位置的明文字节。

您可以在Web应用程序中采用的一种有效缓解策略是，使客户端在给定时间段内（例如，每小时7,200个请求）呈现大量次的会话令牌失效。超过阈值后，服务器使令牌失效，用户必须重新认证。

在高保障环境中，应考虑第二个阈值来锁定用户帐户（例如，24小时内86,400个请求）。Lucky 13攻击需要数天和精心策划才能进行，RC4字节偏差攻击需要数月。在此之前锁定帐户，您可以切实地消除风险。

客户端证书提供了额外的保护层，防止重复使用受损的凭证（例如密码和会话令牌），并建议用于提供纵深防御。

## 评估TLS端点

您可以通过以下方式识别TLS服务中的潜在漏洞：

*   识别TLS库和版本
*   枚举支持的协议和密码套件
*   枚举支持的特性和扩展
*   审查服务器证书

在对服务进行指纹识别并审查其配置后：

*   手动确认已知漏洞
*   评估TLS服务的稳定性

以下我将描述这些步骤并详细说明各个测试策略。

### 识别TLS库和版本

您可以使用操作系统指纹识别和横幅抓取来识别服务器使用的TLS库（在某些情况下还包括版本）。：
- TLS Prober工具[^38]

[^38]: 参见GitHub上的 [TLS Prober](https://github.com/WestpointLtd/tls_prober)。


**表11-7. TLS库和应用程序**

| 库                       | 使用者                                                                     |
|--------------------------|----------------------------------------------------------------------------|
| OpenSSL                  | Apache（通过mod_ssl）和包括Linux在内的许多平台                             |
| NSS                      | Apache（通过mod_nss）和Oracle Solaris企业产品                              |
| GnuTLS                   | Apache（通过mod_gnutls）、Linux、Windows及其他                             |
| Microsoft SChannel       | Microsoft操作系统和产品                                                    |
| Apple Secure Transport   | Apple OS X和iOS                                                            |
| TLS Lite                 | Python应用程序                                                             |
| Oracle JSSE              | Java应用程序和框架，包括Spring MVC                                         |
| Bouncy Castle            | Java和C#应用程序                                                           |

Apache横幅通常会揭示操作系统和TLS库，如下所示：

```log
Server: Apache/2.2.8 (Win32) mod_ssl/2.2.8 OpenSSL/0.9.8g
Server: Apache/2.2.22 (Debian) mod_gnutls/0.5.10 PHP/5.4.4-14+deb7u4
Server: Apache/2.4.10 (Fedora) mod_nss/2.4.6 NSS/3.15.2 Basic ECC PHP/5.5.18
```

注意不要混淆模块和库的版本。在这里，GnuTLS库的版本未知，mod_nss模块的版本（2.4.6）与底层库（NSS 3.15.2）不对应。

### 枚举支持的协议和密码套件

工具：
- Nmap的`ssl-enum-ciphers`脚本	
	Nmap在示例中报告为强的许多其他配置实际上很弱
- [SSLyze](https://github.com/nabla-c0d3/sslyze)

#### 弱密码套件

附录C详细列出了弱密码套件。以下列表总结了它们：

**匿名DH套件**
以匿名模式运行的静态DH（即DH_anon或ECDH_anon）缺乏认证，通过中间人攻击可能进行身份冒充。

**使用空密码的套件**
大多数空密码套件（例如TLS_RSA_WITH_NULL_SHA）执行密钥交换和认证，但以明文形式发送数据。

**出口级套件**
被视为出口级的密码套件使用40位和56位密钥的批量对称加密算法。数据被加密，但较短的密钥长度允许通过暴力破解解密。

**使用弱加密算法的套件**
用于提供批量对称加密的DES、3DES、IDEA、RC2和RC4密码存在已知弱点。尽管针对RC4的字节偏差攻击实际上难以实施（需要生成大量数据），但Microsoft和其他厂商正在从其产品中移除RC4支持。[^40]

[^40]: swiat, [“Security Advisory 2868725: Recommendation to Disable RC4”](http://bit.ly/2a3uTNL), Microsoft TechNet Blog, 2013年11月12日。

#### 首选密码套件顺序

Bojan Zdrnja发布的Nmap `ssl-enum-ciphers`脚本补丁[^42]为每个支持的协议返回密码列表及其偏好（按顺序排列）。

[^42]: 参见GitHub上的 [ssl-enum-ciphers.nse](https://github.com/bojanisc/nmap-scripts)。

偏好顺序至关重要，因为有缺陷的RC4和CBC模式密码不应被优先于安全替代方案。TLS中可用的经过认证的GCM密码（例如AES-GCM）如果正确实现则是安全的，应该被优先选择。

在测试期间，应使用特定的IP地址并多次运行测试，以考虑跨多个后端组件的负载均衡。

### 枚举支持的特性和扩展

通过审查服务器对使用Nmap、OpenSSL命令行工具和SSLyze发送的请求的响应，来枚举TLS特性和扩展的支持情况，详见以下章节。

#### 会话恢复

TLS端点通过会话ID或RFC 5077票据支持恢复。握手泛滥可能导致拒绝服务；因此，许多TLS服务器限制为特定源缓存的会话ID数量。
- SSLyze 测试恢复支持。

#### 会话重新协商

使用SSLyze测试安全重新协商和客户端发起重新协商的支持情况。

#### 列出支持的TLS扩展

除了会话票据、安全重新协商和TLS心跳协议外，服务器可能还支持其他值得注意的TLS扩展。
使用OpenSSL命令行工具枚举使用的TLS扩展

#### 压缩支持

使用SSLyze测试TLS压缩支持。

#### 回退支持

使用OpenSSL命令行工具中的`-fallback_scsv`标志来识别允许会话降级和TLS回退的服务。

### 证书审查

工具：
- `openssl x509 -text -noout`解析X.509证书块
- Nmap `ssl-cert`脚本显示证书信息

在审查证书块时，请确保以下事项：

*   X.509主体通用名称（CN）与服务正确[^43]
*   颁发者是可信的，证书链有效
*   RSA或DSA公钥值大于2048位
*   DH公共参数大于2048位

[^43]: RFC 5280 subjectAltName扩展也可能列主机名。

*   证书有效且未过期
*   证书使用SHA-256签名

#### 私钥已知的X.509证书

工具：
- 已知私钥库：Little Black Box 包含超过2000个私钥已知的证书（主要是Cisco、Linksys、D-Link、Polycom等制造商生产的设备）。
- 已知私钥检查：Nmap使用`ssl-known-key`脚本集成了检查功能，该脚本将证书的哈希与数据库进行交叉引用

#### 不安全生成的证书

如果密钥生成期间使用的值缺乏熵（例如，PRNG实现存在缺陷），多个证书可能共享质数，这可以被攻击。[^45]研究表明，在线2.5%的TLS端点的RSA私钥可能被破坏。

[^45]: Nadia Heninger等人, [“Mining Your Ps and Qs: Detection of Widespread Weak Keys in Network Devices”](https://factorable.net/paper.html), 第21届USENIX安全研讨会论文集，华盛顿州贝尔维尤，2012年8月10-12日。

### TLS端点压力测试

工具：
- `thc-ssl-dos`工具[^46]通过并发握手和客户端发起的重新协商请求（如果服务器支持）对TLS端点进行压力测试
- `sslsqueeze`[^47]，它更强大，并且不依赖重新协商来淹没TLS端点。

[^46]: 参见THC.org上的 [thc-ssl-dos](http://bit.ly/2aFN1xV)。
[^47]: 参见Stunnel上的 [sslsqueeze](http://bit.ly/2aXEIz1)。

与客户端相比，在TLS握手期间执行加密操作会消耗服务器大量的CPU周期。根据配置，工作因子可能高达25（如Vincent Bernat[^48]所讨论）。如果资源耗尽，服务器将无法处理TLS流量，并且其他进程可能受到影响。

[^48]: Vincent Bernat, [“SSL/TLS & Perfect Forward Secrecy”](http://bit.ly/2easGkR), MTU Ninja Blog, 2011年11月28日。

为获得最佳效果，请考虑从具有充足处理能力的高带宽系统（例如，位于托管机房）执行测试。笔记本电脑的CPU和上行宽带带宽将限制攻击的有效性。

Sukalp Bholpe的论文讨论了TLS可用性问题和对抗措施。[^49]他描述了使用`thc-ssl-dos`和`sslsqueeze`的攻击，包括对系统负载的分析。

[^49]: Sukalp Bhople, [“Server-Based DoS Vulnerabilities in SSL/TLS Protocols”](http://bit.ly/2aQvjL9)，硕士论文，埃因霍温理工大学，荷兰埃因霍温，2012年8月。

限制洪水攻击影响的缓解策略包括：

*   禁用对客户端发起会话重新协商的支持
*   使用TLS会话票据扩展以最小化服务器端状态跟踪
*   使用专用加速硬件终止TLS以减轻服务器负载
*   配置端点限制每个源的TLS握手次数

### 手动访问TLS包装的服务

工具：
- Stunnel
- OpenSSL命令行工具的`s_client`模式通过STARTTLS over POP3建立安全通道

## TLS服务评估总结

**识别TLS库和版本**
通过操作系统和网络服务指纹识别，以及审查可用的Apache HTTP Server横幅，尝试识别TLS库和版本（或至少排除未使用的库）。还要考虑服务器上运行的其他软件包（例如SMTP或FTP软件）的发布日期，以缩小特定TLS库候选范围。

**枚举支持的协议和密码套件**
使用Nmap的`ssl-enum-ciphers`脚本列出支持的协议和密码。该脚本的后续版本（在Nmap 7及更高版本中）还应支持STARTTLS，并按服务器偏好排序密码套件。

**列出支持的扩展和特性**
使用Kali Linux中的OpenSSL命令行工具、Nmap和SSLyze识别TLS扩展（例如，对安全重新协商、会话票据和ECC的支持）。

**审查服务器的X.509证书**
确保RSA和DSA公钥大小以及使用的签名算法不弱。还要审查扩展、证书有效期以及证书是否由可信的颁发者签名。

**手动确认漏洞**
将TLS库（以及版本，如果有）与支持的协议、密码套件、特性和扩展进行交叉引用。建立已确认的协议和实现缺陷列表，以了解适用的风险。

**对TLS端点进行压力测试**
如果服务支持客户端发起的重新协商，使用`thc-ssl-dos`工具进行压力测试。如果不支持，使用`sslsqueeze`评估鲁棒性。

## TLS加固

在加固TLS端点时，应考虑以下步骤：

*   将软件升级到最新版本，以缓解已知的实现缺陷
*   禁用对SSL 3.0的支持以缓解POODLE
*   禁用弱加密算法（即RC2、RC4、IDEA、3DES和DES）
*   如果可用，优先选择以下密码套件：
    *   使用ECDHE进行密钥交换（启用前向保密性）的套件
    *   用于批量加密的经过认证的GCM密码（例如AES-GCM）
*   禁用对TLS压缩的支持以缓解CRIME
*   禁用对客户端发起重新协商的支持
*   强制执行最小密钥长度：
    *   RSA和其他非对称模式（例如DSA）为2048位
    *   DH参数为2048位
    *   ECC模式（即ECDHE和ECDSA）为256位
    *   哈希函数（例如SHA-256等）为256位
*   查阅 [http://bit.ly/2aQuKB6](http://bit.ly/2aQuKB6) 以缓解DH弱点
*   如果可用性很重要，避免使用大密钥大小（例如，RSA中用于密钥交换的4096位密钥会带来显著的服务器处理开销）
*   确保私钥以安全的方式生成、处理和存储（例如，不可全局读取，不留放在主目录、版本控制或未加密的备份中）
*   使用信誉良好的CA使用SHA-256签署您的证书

## Web应用程序加固

在加固具有HTTPS组件的Web应用程序时，请考虑以下事项：

*   通过HTTPS提供整个应用程序和资源
*   使用HSTS强制实施传输安全[^51]
*   对于Referer字段不包含当前站点名称的会话，禁用HTTP压缩
*   对客户端呈现大量次数的包含安全令牌（即会话令牌和CSRF令牌）的请求进行速率限制，然后使会话失效，或锁定用户帐户一段时间
*   限制用户提供的令牌或秘密在HTTP响应中的反射

[^51]: 参见 [RFC 6797](https://tools.ietf.org/html/rfc6797)。