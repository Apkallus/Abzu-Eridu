# Kerberos

概念：
- Kerberos（RFC 4120） 是 Microsoft Windows 网络和基于 Unix 环境中使用的认证协议。该协议的一个优点是用户密码不用于与各个服务进行认证；而是使用由密钥分发中心（KDC）生成的加密票据。

- KDC 运行在端口 88，提供认证和票据授予服务。这些机制向客户端提供两种类型的票据：
    - 票据授予票据（TGT）：用于请求服务票据
        - 在 Microsoft 网络中，登录域时 KDC 提供票据授予票据
        - 在基于 Unix 的环境中，调用 `kinit`
    - 各个服务票据：用于访问各个应用程序

    **Kerberos KDC 消息**

    | 消息 | 描述 |
    |------|------|
    | KRB_AS_REQ | 对 TGT 的认证服务请求，包含主体名称和时间戳，使用主体的长期密钥（作为共享秘密）加密 |
    | KRB_AS_REP | 使用共享秘密解密时间戳后，认证服务释放一个包含会话密钥的 TGT，使用主体的长期密钥加密；TGT 还包含一个使用 KDC 主密钥加密的票据块 |
    | KRB_TGS_REQ | 票据授予服务请求，其中 TGT 与对特定服务的访问请求组合在一起，使用会话密钥加密 |
    | KRB_TGS_REP | 验证请求后，票据授予服务生成一个共享会话密钥（将在客户端和服务器之间使用），使用目标服务器的长期密钥加密一份副本，并创建一个服务票据发送给客户端（使用原始会话密钥加密） |
    | KRB_AP_REQ | 客户端向目标服务器提供服务票据，服务器使用其长期密钥解密并获得共享会话密钥，解密并验证票据本身，然后授予访问权限 |
    | KRB_AP_REP | 用于相互认证场景的可选消息，服务器使用共享会话密钥加密时间戳值 |
    | KRB_ERROR | 用于从服务器向客户端发送错误消息，并使用特定加密诱导认证，或通信异常 |
    | KRB_SAFE | 用于传输带有校验和的数据（提供完整性） |
    | KRB_PRIV | 用于传输带有校验和和加密的数据 |
    | KRB_CRED | 用于将票据转发给其他主体 |


攻击面：此无状态协议中，票据描述了用户权限
- 若 KDC 使用的主密钥被泄露，攻击者可创建任意票据，称为**黄金票据**。
- 若主体密码、密钥或票据被泄露，攻击者可生成票据并访问服务。

Alva Duckwall 和 Benjamin Delpy 在 Black Hat USA 2014 的演讲[^63] 详细介绍了这些场景，Fulvio Ricciardi 对 Kerberos 协议的描述是一个极好的资源[^64]。


[^63]: Alva Duckwall and Benjamin Delpy，“Abusing Microsoft Kerberos - Sorry You Guys Don’t Get It”，在 Black Hat USA 2014 上展示，内华达州拉斯维加斯，2014 年 8 月 2-7 日。
[^64]: 参见 ZeroShell Net Services 上的 Kerberos 协议及其实现。

Kerberos 术语使用**主体**来描述 realm 内的实体（即用户、系统、应用程序和服务）。为生成票据，KDC 和主体使用共享秘密，这些是**长期密钥**，通常从密码派生（例如用户或计算机账户密码）。

Kerberos realm 中使用的长期密钥如下：

- **KDC 主密钥（认证服务主体长期密钥）**：在 Windows AD 服务器中，这些值从本地 `krbtgt` 账户的密码派生。

- **主体长期密钥**：客户端和服务器都使用与 KDC 共享的长期密钥，用于加密票据。密钥通常从密码派生，与 KDC 主密钥一样，可以使用不同的函数进行哈希。

## 票据格式

Kerberos 票据包含一个使用认证服务长期密钥（即 KDC 主密钥）或各个服务主体（如网络服务或应用程序）长期密钥加密的票据块。Microsoft 的实现包含一个**特权属性证书（PAC）** 数据结构，该结构经过签名，并包含用户名、域、用户和组详细信息。

Microsoft Kerberos 票据结构，由 KDC 进行加密
- TGT 使用认证服务密钥
- 服务票据使用特定服务主体密钥

**表 7-25. Kerberos 票据字段** 
前三个字段是明文，其余票据块加密

| 字段 | 描述 |
|------|------|
| 版本号 | 票据格式使用的 Kerberos 版本 |
| Realm | 颁发票据的 realm（域）名称 |
| 服务器名称 | 目标服务主体名称和 realm |
| 标志 | 票据的选项（可转发、可续期、无效等） |
| 密钥 | 用于加密后续消息的会话密钥 |
| 客户端 realm | 请求者的 realm |
| 客户端名称 | 请求者的主体名称 |
| 传递列表 | 如果使用跨 realm 认证，则为 Kerberos realm 列表 |
| 认证时间 | 初始认证事件的时间戳 |
| 开始时间 | 票据生效的时间 |
| 结束时间 | 票据的过期时间 |
| 续期截止 | 可选，票据可以续期的截止时间 |
| 客户端地址 | 可选，可以使用票据的地址列表 |
| 授权数据 | 客户端的授权数据——在 Microsoft 实现中，这包含定义用户名、域和 SID 值的 PAC 数据结构；在 MIT Kerberos 中，此字段通常包含应强制执行的对客户端的限制 |

### Microsoft PAC 字段

https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-pac/

PAC 位于加密票据中的授权数据内。PAC 中有用的字段位于 `KERB_VALIDATION_INFO` 结构下，包括用户名、域和组成员详细信息。

### 票据块加密和签名

TGT 使用用户主体长期密钥进行加密以防止窃听。解密 TGT 后，获得会话密钥，并缓存加密的票据块。然后使用会话密钥加密服务票据，服务票据包含一个加密的票据块。

**Microsoft Kerberos 票据块加密和签名**

| | 票据块加密 | PAC 签名（KDC） | PAC 签名（服务器） |
|--|------------|----------------|-------------------|
| 票据授予票据（TGT） | `krbtgt` | `krbtgt` | `krbtgt` |
| 服务票据 | `target` | `krbtgt` | `target` |

在 TGT 中，Microsoft KDC 服务器对 PAC 数据结构进行签名以防止篡改。由于目标服务器必须验证服务票据中的 PAC，KDC 对 PAC 签名两次，首先使用认证服务的长期密钥，然后使用目标服务器的长期密钥。

一旦泄露 KDC 认证服务（`krbtgt`）的长期密钥，你可以生成任意的 TGT（黄金票据）。掌握了服务主体（目标）的长期密钥后，你可以修改服务票据以生成包含伪造 PAC 结构的**白银票据**[^67]。

[^67]: 详情请参见 Ben Lincoln，“Mimikatz 2.0—Silver Ticket Walkthrough”，Beneath the Waves Blog，2014 年 12 月 18 日。

## Kerberos 攻击面

KDC 功能运行在端口 88 上，用户管理和密码管理端口为 464，MIT 实现中还暴露了一个用于管理目的的额外端口。

**Kerberos 网络服务**

| 端口 | 协议 | 名称 | Microsoft | MIT | 描述 |
|------|------|------|-----------|-----|------|
| **TCP** | **UDP** | | | | |
| 88 | ● | ● | kerberos | ● | ● | Kerberos 认证服务 |
| 464 | ● | ● | kpasswd | ● | ● | Kerberos 密码服务 |
| 749 | ● | ● | kerberos-adm | – | ● | Kerberos 管理服务 |

## 本地攻击

具有本地系统或网络访问权限的攻击者可以采用以下策略：

- 被动网络嗅探 Kerberos 认证服务请求
- 通过 MITM 进行主动降级攻击以削弱加密
- 泄露 KDC 主密钥，导致生成黄金票据
- 泄露用户密钥和票据，这些可以被修改、传递和重用

在 Windows 域中进行横向移动的攻击者采用这些策略，因为大多数环境出于兼容性原因支持弱加密类型。密钥捕获和重用也使攻击者能够维持访问（直到密钥更改）。

### 被动网络嗅探

使用 Arne Vidstrom 的 `kerbcrack` 收集认证服务请求并暴力破解账户密码。Cain & Abel 和 John the Ripper 也支持捕获和离线暴力破解通过 Kerberos 获得的密码哈希。

### 主动降级和离线暴力破解

通过 MITM 降级传输安全，并破解账户密码。

列出了常见的 Microsoft Windows 加密类型（称为 Etypes），这些是用于生成长期密钥和执行认证的哈希函数。服务器默认禁用对弱加密的支持；然而，支持此类 Etypes 的客户端可能被诱骗向恶意 KDC 发送 `KRB_AS_REQ` 材料，然后这些材料容易受到暴力攻击。RFC 6113 演示了 Kerberos 网络数据包捕获和推荐的加固步骤。

**Microsoft Windows Kerberos Etypes**

| 加密类型 | 强度 | 支持的操作系统 |
|----------|------|----------------|
| AES256-CTS-HMAC-SHA1-96 | 256 位 | Windows Server 2008 R2；Windows 7 |
| AES128-CTS-HMAC-SHA1-96 | 128 位 | Windows Server 2008；Windows Vista |
| RC4-HMAC | | Windows 2000 |
| DES-CBC-MD5 | 56 位 | Windows XP |
| DES-CBC-CRC | | |
| RC4-HMAC-EXP | 40 位 | |

创建一个实用程序来注入 `ERR_PREAUTH_REQUIRED` 消息，捕获后续哈希，并通过 John the Ripper 破解它们。

Microsoft 在 Windows 8 和 Server 2012 中引入了 **Kerberos armoring**——通过使用计算机账户的密钥加密 `KRB_AS_REQ` 消息，为消息提供传输层安全。Armoring 缓解了 MITM 和离线字典攻击，然而，运行在 Windows Server 2012 域功能级别以下的系统仍然存在漏洞。

### 密码哈希、Kerberos 密钥和票据泄露

在 Windows 环境中，攻击者使用 **Mimikatz** 提取 NTLM 用户密码哈希、Kerberos 长期密钥和票据。
根据系统配置，效果会有所不同。，如下文所述。

使用 Mimikatz 导出 Kerberos 票据，然后可以重用和传递密钥和票据

Windows 8.1 和 Server 2012 R2 中的 Microsoft 域保护用户功能限制了这种对 Kerberos 票据的暴露，减轻了从内存中提取长期密钥和用户密码哈希的风险。

**票据传递**：密码和关联的主体长期密钥用于与 KDC 认证并生成 TGT。使用票据，你可以访问 Kerberos realm 内暴露的应用程序和服务。

在获取并导出 `kirbi` 格式的有用票据后，使用 Mimikatz 中的 `ptt`（pass-the-ticket）指令将它们加载到内存中并与服务交互。Sean Metcalf 的论文[^74] 详细介绍了这些策略和 Mimikatz 语法。

[^74]: Sean Metcalf，“Mimikatz and Active Directory Kerberos Attacks”，Active Directory Security，2014 年 11 月 22 日。


**使用 Mimikatz 将 Kerberos 票据加载到内存中**

```sh
mimikatz # kerberos::ptt 1-40e10000-uberuser@krbtgt~ABC.ORG-ABC.ORG.kirbi
mimikatz # kerberos::ptt 2-40a50000-uberuser@cifs~dc1.abc.org-ABC.ORG.kirbi
```

**通过 PsExec 执行特权命令**

```bash
C:\Users\notanadmin> psexec \\dc1.abc.org cmd.exe
C:\Windows\system32> whoami
abc\uberuser
```

**使用长期密钥更改用户密码**。Aorato 的 Tal Be’ery 公开了 Kerberos 中的一个设计缺陷，通过该缺陷，你可以与管理和密码管理接口（通过端口 464）交互，并仅使用主体的长期密钥设置任意密码[^75]。

[^75]: Sean Michael Kerner，“Aorato Uncovers Critical Microsoft Active Directory Vulnerability”，eWEEK，2014 年 7 月 15 日。

## 未认证的远程攻击

如果你无法访问 Kerberos 流量或系统本身，可以应用的远程攻击向量包括 realm 枚举、用户名枚举和暴力密码猜测。

### Realm 枚举

Kerberos 服务通常由 DNS 支持：
- DNS 的 SRV 条目记录 Kerberos 服务的端点
- 域内与 `_kerberos` 名称关联的 TXT 记录描述了 realm

**使用 dig 进行 Kerberos realm 枚举**

```bash
dig txt _kerberos.mit.edu +short
"ATHENA.MIT.EDU"

dig txt _kerberos.megacz.com +short
"MEGACZ.COM"
```

### 用户名枚举

有了有效的 realm（例如 Windows 环境中的域名），使用 Nmap 的 `krb5-enum-users` 脚本通过 Kerberos 枚举有效用户账户。

### 暴力密码猜测

使用 `ebrute` 实用程序对 KDC 执行暴力密码猜测。Hydra 和其他实用程序似乎不支持通过 Kerberos 进行主动暴力破解。

## 待阅读归档

文章：
- [2026 - Bypassing Windows authentication reflection mitigations for SYSTEM shells](https://halloween.synacktiv.com/en/publications)

工具：
- [ghostSPN](https://github.com/mverschu/ghostSPN) 用于识别 Active Directory 中的“幽灵”服务主体名称 (SPN)。它可以发现攻击者可以利用的过时或孤立的 SPN，这些 SPN 可用于基于 Kerberos 的权限提升。