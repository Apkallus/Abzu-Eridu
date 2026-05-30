# SNMP

概念
- 简单网络管理协议（SNMP）服务通常运行在可管理的交换机、路由器和服务器操作系统（例如 Microsoft Windows Server 和 Linux）上，用于监控目的提供系统详细信息。
- 端口
    - SNMP 通过在 UDP 数据报中向端口 161 提供有效的团体字符串进行访问。
    - SNMPv3 服务器也可以运行在 TCP 端口 161 上，并使用 TLS 提供传输安全。
    
- 大多数服务器配置有两个团体字符串：一个提供对 SNMP 管理信息库（MIB）的只读访问，另一个提供读写访问。
    - MIB 是对象标识符（OID）值的层次结构


工具
- `snmpwalk`
    - 额外启用 OID 条目的描述解析
        ```bash
        apt install snmp-mibs-downloader # 下载 MIB 数据
        echo "" > /etc/snmp/snmp.conf # 覆盖指令
        ```
    - 使用 `-v` 标志指定协议版本

SNMP 协议版本

| 版本 | 认证 | 传输安全（可选） |
|------|------|------------------|
| 1 | 团体字符串 | 无 |
| 2 | 团体字符串 | 无 |
| 3 | 用户名和密码，使用 MD5 或 SHA-1 哈希 | 168 位 3DES 或 256 位 AES |

## 利用 SNMP

可访问的 SNMP 服务器可以提供有关特定系统的大量信息，甚至可能使远程设备被攻陷。
    
    若获得 Cisco 路由器的读/写 SNMP 社区字符串，就可下载路由器的整个配置、修改它，然后将其上传回路由器。（社区字符串本质上是用于查询设备信息或将配置信息写入设备的密码。）

攻击面
- 通过 SNMPv3 枚举用户
    - `snmpv3enum` 工具
- 暴力猜测团体字符串和用户密码值
    - 工具
        - `Hydra` 工具支持对 SNMP 版本 1、2 和 3 进行暴力猜测
        - MSF `snmp_login` 模块进行社区字符串字典猜测
    - 字典
        - V1/2 团体字典：MSF `wordlists/snmp_default_pass.txt` 
        - V3 默认用户名/密码组合：https://github.com/ihebski/DefaultCreds-cheat-sheet
- 通过读取 SNMP 数据暴露有用信息（低权限）
- 通过写入 SNMP 数据进行利用（高权限）
- 利用软件实现缺陷，导致意外后果（例如特权远程代码执行）


### 通过 SNMP 暴露有用信息

通过 SNMP 可获得有用的信息（例如监听的网络服务、运行的进程、用户名和内部 IP 地址）。

通过对特定 OID 值进行 walk 来枚举 Microsoft Windows 系统上的用户名。

通过 SNMP 枚举 Windows 账户

```bash
root@kali:~# snmpwalk -c public 192.168.102.251 .1.3.6.1.4.1.77.1.2.25
```

有用的 Microsoft Windows SNMP OID 值

| OID | 收集的信息 |
|-----|------------|
| `.1.3.6.1.2.1.1.5` | 主机名 |
| `.1.3.6.1.4.1.77.1.4.2` | 域名 |
| `.1.3.6.1.4.1.77.1.2.25` | 用户名 |
| `.1.3.6.1.4.1.77.1.2.3.1.1` | 运行的服务 |
| `.1.3.6.1.4.1.77.1.2.27` | 共享信息 |

包括密码和可写团体字符串在内的秘密常常通过 SNMP 暴露。因此，在测试期间应手动审查 MIB 内容。Metasploit `snmp_enum` 模块也能提取有用的数据。

Linux 服务器通过 SNMP 获取内部网络详细信息

```bash
root@kali:~# snmpwalk -v 1 -c public 60.56.160.15
```

### 通过写入 SNMP 破坏设备

在获得 SNMP 写入访问权限后使用 MSF 的 `cisco_config_tftp` 与 `cisco_upload_file` 模块，以读取运行配置并将文件上传到 Cisco 设备。两者都启动一个 TFTP 服务器，并覆盖目标 MIB 中的值以引发文件上传或下载（要求目标主机可访问 TFTP 服务）。

Daniel Mende 的 `snmpattack.pl`[^44] 在测试中也可能有用。

这种攻击的扩展是使用 UDP 欺骗。如果目标设备上监听的 SNMP 服务具有 ACL 并且不响应从你的地址发送的数据包，你可以欺骗 SNMP 命令，使其看起来来自受信任的主机（例如防火墙的外部 IP 地址或内部管理系统）。

### 已知的 SNMP 实现缺陷

拒绝服务
权限提升
