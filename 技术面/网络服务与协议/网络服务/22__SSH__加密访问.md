# SSH

概念：
- SSH 服务为包括嵌入式设备和基于 Unix 的主机在内的系统提供加密访问。通常向用户公开的三个子系统如下：

    - **安全 Shell（SSH）**：提供命令行访问
    - **安全复制（SCP）**：允许用户发送和检索文件
    - **安全 FTP（SFTP）**：提供功能丰富的文件传输

- 默认使用 TCP 端口 22 公开 SSH 及其子系统。SSH 还支持网络连接的隧道和转发；因此，你可以将其用作 VPN 来安全地访问资源。

工作方式：

- 使用 Diffie-Hellman 密钥交换建立共享秘密
- 客户端和服务器均使用伪随机函数（例如 SHA-1 或 SHA-256）从共享秘密派生三对密钥（每方一对）：
    - 两个初始化向量（IV）值
    - 两个加密密钥
    - 两个签名密钥
- 服务器将其公钥以及一个随机签名值发送给客户端
- 客户端验证随机值的签名（认证服务器）
- 服务器对客户端进行身份验证
- 认证后，建立通道以提供对资源的访问


攻击面：

- 暴力密码猜测
- 由于私钥泄露或密钥生成弱点而被授予访问权限
- 远程匿名利用已知软件缺陷（无需凭据）
- 认证后利用已知缺陷，导致权限提升

许多缺陷的实际利用依赖于启用或使用某些功能。因此，调查和了解服务配置非常重要。

## 指纹识别

方式：
- SSH 服务器在连接时返回的横幅。
    - 注重安全的管理员有时会修改横幅，仍然显示服务器支持的协议版本，但隐藏实现。
    - MSF `auxiliary/scanner/ssh/ssh_version`

- 获取 RSA 和 DSA 主机密钥，而 SSH 密钥通常是唯一的
    - Nmap 的 `ssh-hostkey` 脚本从服务器检索公钥值，可用于识别多宿主系统。


## 枚举功能

使用 Nmap 和详细模式下的 OpenSSH 客户端调查暴露的 SSH 服务将揭示支持的算法和认证机制。

### 支持的算法

SSH 使用握手来执行密钥交换、认证以及加密算法的选择。通过 Nmap `ssh2-enum-algos` 脚本枚举密钥交换、认证、加密和完整性检查的受支持算法。

这些算法和特性也在 TLS 中使用。SSH 中可利用的协议弱点源于以下方面：

- 使用不安全群组进行密钥交换：  
    密钥交换算法 `diffie-hellman-group1-sha1`，使用固定的 1024 位参数（也称为群组）。

- 使用不安全的椭圆曲线进行密钥交换：
    椭圆曲线 Diffie-Hellman（ECDH）：使用某些 NIST 曲线（即 `ecdh-sha2-nistp256`、`ecdh-sha2-nistp384` 和 `ecdh-sha2-nistp521`）的 ECDH 密钥交换特别不安全，会导致中间人攻击。
    

### 支持的认证机制

使用详细模式下的 OpenSSH 客户端枚举支持的认证机制的顺序

    ```sh
    ssh -v 占位符
    ```

**表 7-7. 常见的 SSH 认证机制**

| 名称 | 描述 |
|------|------|
| `publickey` | 公钥用户认证（使用 DSA、ECDSA 或 RSA） |
| `hostbased` | 基于主机的公钥认证 |
| `password` | 用户密码认证 |
| `keyboard-interactive` | 通过 PAM 的认证抽象层（例如 Google Authenticator、YubiKey、Duo Security） |
| `gssapi-with-mic` | GSSAPI 认证 |
| `gssapi-keyex` | |

连接的 `keyboard-interactive` 模式配置是在连接时推断的。例如，该模式可能提示用户输入密码（即常规 PAM 认证）、认证令牌值或对挑战的响应。

### 枚举有效密钥

硬件制造商出货的设备带有默认凭据，其他制造商则因代码库中引入的后门而遭受攻击

流程
- 收集 SSH 密钥列表或特定身份验证绕过载荷
    - https://github.com/rapid7/ssh-badkeys
    - https://github.com/ihebski/DefaultCreds-cheat-sheet
    - CVE-2026-35414 字段解析漏洞
    
- 公钥识别
    使用 Metasploit `ssh_identify_pubkeys` 模块测试可访问的 SSH 服务并识别有效密钥。
- 私钥猜测登录
    Hydra 的 `sshkey` 模式


## 不安全生成的主机密钥

如果 RSA 或 DSA SSH 主机密钥对生成不安全（例如使用熵不足的 PRNG），攻击者可以计算私钥，并通过中间人攻击冒充合法的服务器端点。

RSA 公钥由两个整数组成：指数 `e` 和模数 `n`。模数是两个选定素数（`p` 和 `q`）的乘积。私钥是解密指数 `d`，如下所示：

```
d = e⁻¹ mod (p - 1)(q - 1)
```

如果攻击者知道 `n` 的因式分解，他们可以计算任何公钥 `(e, n)` 的私钥。当 `p` 和 `q` 未知时，最有效的已知方法是将 `n` 分解为两个素数以计算私钥 `d`。

当找到两个共享单个素数（无论是 `p` 还是 `q`）的不同 RSA 模数 `(n₁, n₂)` 时存在漏洞——攻击者可以计算最大公约数并发现另一个素数（例如，如果共享 `p`，则发现 `q₁` 和 `q₂`）[^26]。通过扫描互联网，该团队能够攻破在线 SSH 服务器使用的 0.03% 的 RSA 主机密钥和 1% 的 DSA 密钥。

[^26]: 该方法详见 Nadia Heninger 等人，“Missing Your Ps and Qs: Detection of Widespread Weak Keys in Network Devices”，第 21 届 USENIX 安全研讨会论文集，华盛顿州贝尔维尤，2012 年 8 月 8-10 日。

https://www.exploit-db.com/exploits/5720 上的 SSH 可预测 PRNG 漏洞。

## SSH 服务器软件缺陷

在了解 SSH 服务器配置（即运行的软件、支持的协议和认证机制）后，通过搜索 NVD 和其他来源查找已知漏洞。