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

