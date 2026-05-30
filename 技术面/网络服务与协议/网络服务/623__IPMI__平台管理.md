# IPMI

概念：
- 基板管理控制器（BMC）是嵌入式计算机，为台式机和服务器提供带外监控。BMC 产品以许多品牌名称销售，包括 HP iLO、Dell DRAC 和 Sun ILOM。
- 通常通过 UDP 端口 623 公开 IPMI 服务

识别：
- 使用单数据包探测进行网络扫描
    - Metasploit `auxiliary/scanner/ipmi/ipmi_version` 模块

攻击面：
- 通过 RAKP 远程获取密码哈希
    - Metasploit `auxiliary/scanner/ipmi/ipmi_dumphashes` 模块
    - 之后使用 Hashcat 或 John the Ripper 破解用户密码哈希
- 零密码身份验证绕过，导致管理访问
    - Metasploit `ipmi_cipher_zero` 模块
    - `ipmitool` 客户端工具手动与服务交互并绕过身份验证（通过 `-C 0` 选项）。