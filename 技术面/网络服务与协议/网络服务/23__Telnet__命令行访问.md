# Telnet

概念：
- Telnet 提供对服务器和嵌入式设备的命令行访问。该协议没有传输安全，具有网络访问权限的攻击者可以被动嗅探或主动劫持会话。

攻击面：
- 暴力密码猜测，揭示弱密码或默认凭据
- 匿名利用 Telnet 服务器软件缺陷（无需凭据）

指纹识别
- Nmap 
- `telnet` 手动连接

## 默认 Telnet 凭据

网络打印机、宽带路由器和可管理交换机通常可以使用默认管理凭据访问。

使用默认密码列表测试暴露的 Telnet 服务器
- https://github.com/ihebski/DefaultCreds-cheat-sheet

## Telnet 服务器软件缺陷

Siemens 和 Cisco 制造的设备以及 FreeBSD、Oracle Solaris 和 Microsoft Windows 等操作系统中的 Telnet 服务器漏洞。
