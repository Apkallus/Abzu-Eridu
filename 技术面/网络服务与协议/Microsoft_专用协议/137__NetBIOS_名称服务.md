# NetBIOS 名称服务

概念
- NetBIOS 名称服务向传统 Microsoft 网络中的客户端提供名称表条目——描述本地系统配置、可用服务、父域和域控制器的位置。

工具
- Nmap

    ```bash
    nmap -Pn -sU -sC -p137 192.168.1.5
    ```

NetBIOS 名称表条目，包括运行服务的详细信息和网络中域控制器的位置

| 值 | 后缀 | 类型 | 服务描述 |
|------|------|------|------------|
| `<domain name>` | 00 | G | 域名 |
| `<computer name>` | 00 | U | 工作站 |
| `<computer name>` | 01 | U | 信使服务 |
| `__MSBROWSE__` | 01 | G | 主浏览器 |
| `<computer name>` | 03 | U | 信使服务（为此计算机） |
| `<username>` | 03 | U | 信使服务（为此用户） |
| `<computer name>` | 06 | U | RAS 服务器 |
| `<domain name>` | 1B | U | 域主浏览器名称 |
| `<domain name>` | 1C | G | 域控制器列表 |
| `<INet-Services>` | 1C | G | Microsoft IIS |
| `<domain name>` | 1D | U | 网络的浏览器主名称 |
| `<domain name>` | 1E | G | 浏览器服务选举 |
| `<computer name>` | 1F | U | NetDDE |
| `<computer name>` | 20 | U | 文件服务器 |
| `<computer name>` | 21 | U | RAS 客户端 |
| `<computer name>` | 22 | U | Microsoft Exchange 交换 |
| `<computer name>` | 23 | U | Microsoft Exchange 数据存储 |
| `<computer name>` | 24 | U | Microsoft Exchange 目录 |
| `<computer name>` | 2B | U | IBM Lotus Notes |
| `IRISMULTICAST` | 2F | G | IBM Lotus Notes |
| `<computer name>` | 30 | U | 调制解调器共享服务器 |
| `<computer name>` | 31 | U | 调制解调器共享客户端 |
| `IRISNAMESERVER` | 33 | G | IBM Lotus Notes |
| `<computer name>` | 42 | U | McAfee 防病毒 |
| `<computer name>` | 43 | U | SMS 客户端远程控制 |
| `<computer name>` | 44 | U | SMS 远程控制工具 |
| `<computer name>` | 45 | U | SMS 客户端远程聊天 |
| `<computer name>` | 46 | U | SMS 客户端远程传输 |
| `<computer name>` | 4C | U | DEC Pathworks TCP/IP |
| `<computer name>` | 52 | U | DEC Pathworks TCP/IP |
| `<computer name>` | 6A | U | Microsoft Exchange IMC |
| `<computer name>` | 87 | U | Microsoft Exchange MTA |
| `<computer name>` | BE | U | 网络监控代理 |
| `<computer name>` | BF | U | 网络监控实用程序 |