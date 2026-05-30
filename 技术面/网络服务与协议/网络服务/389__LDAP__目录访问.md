# LDAP

概念：
- LDAP 是一个开放协议，通过 IP 提供目录信息服务。目录服务提供有关网络中用户、系统、网络、服务和应用程序的信息。

- 轻量级目录访问协议（LDAP）服务通常运行在 Microsoft Active Directory、Exchange 和 IBM Domino 服务器上。在 Active Directory 中，LDAP 服务称为全局目录。

- LDAP 服务端口

    | 端口 | 协议 | TLS | 名称 | 描述 |
    |------|------|-----|------|------|
    | **TCP** | **UDP** | | | |
    | 389 | ● | ● | – | ldap | LDAP |
    | 636 | ● | – | ● | ldaps | LDAP over TLS |
    | 3268 | ● | – | – | globalcat | Microsoft 全局目录 |
    | 3269 | ● | – | ● | globalcats | LDAP over TLS |


攻击面：
- 通过匿名绑定泄露信息
- 暴力密码猜测
- 认证后修改 LDAP 目录中的数据
- 利用 LDAP 服务器软件缺陷（有或无凭据）

## LDAP 认证

客户端在连接服务器时使用两种认证方法之一（RFC 4513）：

- **简单（Simple）**：简单认证在 LDAP 绑定请求中发送明文凭据。如果执行匿名绑定操作，则不提供凭据。

- **SASL**：简单认证和安全层 SASL （RFC 4422） 提供对 DIGEST-MD5 和 CRAM-MD5 等认证机制的支持。

图 7-2 展示了 SASL 如何作为暴露服务（例如 SMTP 和 XMPP）与认证提供者之间的抽象层。

表 7-19. SASL 常见认证机制

| 机制 | 说明 |
|------|------|
| CRAM-MD5 | MD5 质询-响应认证机制[^49]。此方法容易受到已知明文攻击，包括 Cain & Abel 在内的工具可以在嗅探质询-响应数据后破解密码 |
| DIGEST-MD5 | 摘要 MD5 认证，服务器发送质询和 nonce 值，客户端使用用户名、密码和 realm 组合派生的密钥进行哈希[^50] |
| GSSAPI | 通过 GSSAPI 进行 Kerberos 认证[^51] |
| GSS-SPNEGO | 通过 GSSAPI 进行 Microsoft 协商认证 |
| NTLM | Microsoft NTLM 认证[^52] |
| OTP | 一次性密码[^53] |
| PLAIN | 使用 base64 编码的明文认证 |

[^49]: 参见 RFC 2195。
[^50]: 参见 RFC 2617。
[^51]: 参见 RFC 4752。
[^52]: 参见 Microsoft Developer Network 上的“4.1 SMTP Client Successfully Authenticating to an SMTP Server”。
[^53]: 参见 RFC 2444。

## LDAP 操作

| 操作 | 描述 |
|------|------|
| BIND | 与 LDAP 认证 |
| SEARCH | 搜索目录 |
| COMPARE | 测试条目是否包含给定的属性值 |
| ADD | 添加新条目 |
| DELETE | 删除条目 |
| MODIFY | 修改条目 |
| MODIFY DN | 移动或重命名 DN |
| ABANDON | 中止先前的请求 |
| EXTENDED | 扩展操作 |
| UNBIND | 关闭连接 |

大多数操作在认证后生效。

消息层
- ↓ LDAP
- ↓ SASL
- ↓ TLS
- ↓ TCP/IP

可通过 `STARTTLS` 命令在现有的 LDAP 通道（即 TCP 端口 389）上运行 TLS，也可以通过专用的 LDAPS 端口（如 TCP 端口 636）运行 TLS。

工具：
- OpenLDAP 实用程序包（`openldap-utils`）包含执行 LDAP 操作以及扩展操作（例如更改 LDAP 用户密码）的客户端。

## LDAP 目录结构

目录由 X.500 属性组成（RFC 4519）。在 LDAP 层次结构中，四个属性定义了父域、组织、组织单位（OU）和对象（例如用户或单个系统）

**LDAP 中使用的 X.500 属性**

| 属性 | 描述 | 示例 |
|------|------|------|
| DC | 域组件 | `dc=example,dc=com` |
| O | 组织 | `o=Example LLC` |
| OU | 组织单位名称 | `ou=Marketing` |
| CN | 通用名称 | `cn=John Smith` |

在 LDAP 中，**可分辨名称（DN）** 是到对象的完整路径，从左到右——从详细到宽泛（结构类似域名）。例：

```log
cn=John West,ou=Engineering,dc=example,dc=com
cn=Sally Stevens,ou=Sales,dc=example,dc=com
```

其他属性（例如 `telephoneNumber` 和 `roomNumber`）可以定义与各个对象相关的值。你可以以这种方式定义用户密码哈希、命令 shell、UID 值和其他变量。Microsoft Active Directory 中的结构和属性通常包括以下内容：

- 域、用户、组和 OU
- 组策略对象（附加到 OU 以强制执行特定策略）
- 系统（即工作站、服务器和网络设备）
- 服务器应用程序和功能
- 站点和网络（用于 Microsoft Exchange 中的邮件路由）

## 指纹识别和匿名绑定

Nmap 用于对暴露的 LDAP 服务进行指纹识别和查询。根据服务器配置，或可访问根 DSE 对象并通过匿名绑定搜索 LDAP 目录。

```bash
nmap -Pn -sV -p389 --script ldap-rootdse,ldap-search 50.116.56.5
```

根 DSE 对象包含许多属性(RFC 2251-3.4)，包括服务器已知的命名上下文和子模式、支持的认证机制、扩展和控制。

支持的控件和扩展通过 OID 值描述。IANA 在线维护一个列表[^56]。

[^56]: 参见 IANA.org 上的“Lightweight Directory Access Protocol (LDAP) Parameters”。

**LDAP 控件和扩展 OID 值**

| OID | 描述 | 参考 |
|-----|------|------|
| `2.16.840.1.113730.3.4.18` | 代理授权控制 | RFC 4370 |
| `2.16.840.1.113730.3.4.2` | ManageDsaIT | RFC 3296 |
| `1.3.6.1.4.1.4203.1.10.1` | 子条目 | RFC 3672 |
| `1.2.840.113556.1.4.319` | 分页结果控制 | RFC 2696 |
| `1.2.826.0.1.3344810.2.3` | 匹配值控制 | RFC 3876 |
| `1.3.6.1.1.13.2` | LDAP 后读控制 | RFC 4527 |
| `1.3.6.1.1.13.1` | LDAP 前读控制 | |
| `1.3.6.1.1.12` | 断言控制 | RFC 4528 |
| `1.3.6.1.4.1.4203.1.11.1` | 修改密码 | RFC 3062 |
| `1.3.6.1.4.1.4203.1.11.3` | Who am I? | RFC 4532 |
| `1.3.6.1.1.8` | 取消操作 | RFC 3909 |

## 暴力密码猜测

LDAP 执行暴力密码猜测工具
- Nmap `ldap-brute` 脚本
- Hydra
- `ebrute` 

如果使用严格的安全策略，通过 LDAP、Kerberos 和其他向量进行暴力密码猜测通常会锁定账户。本地 Windows Administrator 账户默认不锁定，在大多数情况下是一个有吸引力的目标。在考虑暴力破解之前，请先枚举环境中使用的安全策略。

## 获取敏感数据

认证后，你可以通过 LDAP 暴露有用的详细信息，包括电话号码、组成员详细信息以及用户密码哈希（通过 `userPassword` 和 `sambaNTpassword` 等属性）

工具
- `ldapsearch` 获取被 LDAP 服务器暴露的密码哈希，
    - 之后使用 John the Ripper 破解

## LDAP 服务器实现缺陷

拒绝服务
本地权限提升