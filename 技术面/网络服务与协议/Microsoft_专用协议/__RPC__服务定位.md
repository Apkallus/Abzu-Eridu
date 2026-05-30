# Microsoft RPC 服务

概念
- Windows 服务通过 TCP、UDP、HTTP 和 SMB 传输协议暴露 RPC 接口。RPC 定位器向客户端（例如 Outlook）提供已注册服务的详细信息。
- 使用四种协议序列访问 RPC 定位器服务：

    - `ncacn_ip_tcp` 和 `ncadg_ip_udp`（TCP 和 UDP 端口 135）
    - `ncacn_np`（通过 SMB 的 `\pipe\epmapper` 命名管道）
    - `ncacn_http`（通过 TCP 端口 80、593 等的 RPC over HTTP）

## 识别暴露的 RPC 服务

查询 RPC 定位器服务和各个 RPC 端点，以分类通过 TCP、UDP、HTTP 和 SMB（通过命名管道）运行的有趣服务。通过此过程收集的每个 IFID 值表示一个 RPC 服务（例如 `5a7b91f8-ff00-11d0-a9b2-00c04fb6e6fc` 是 Messenger 接口）。

工具
- rpcdump
    `rpcdump [-v] [-p protseq] target`
    - `-p` 标志指定连接时使用的特定序列。若未指定则尝试所有
    - `-v` 显示详情

- ifids
    当无法连接到 RPC 定位器服务，使用 `ifids` 查询动态高端口（即运行在 TCP 或 UDP 端口 1024 及以上的端口）并直接枚举 IFID 值

    `ifids [-p protseq] [-e endpoint] target`
    - `-p` 选项指定要使用的协议序列
    - `-e` 定义端口

- Nmap



调查 IFID 值已知的暴露。Jean-Baptiste Marchand 还汇编了一系列详细说明 RPC 接口和命名管道的文档[^5]。

[^5]: Jean-Baptiste Marchand, “Windows Network Services Internals”, Hervé Schauer Consultants, 2003 年 10 月 22 日。


Windows Server 2012、Server 2008 R2 SP1 及其他版本中的 RPC 服务器本身存在一个可远程利用的缺陷，通过该缺陷，认证用户可以在未修补的服务器上以提升的权限执行任意代码（CVE-2013-3175）。

### 查询 LSARPC 和 SAMR 接口



**在建立 SMB 会话（通常需要凭据）后，有用的 rpcclient 命令**

| 命令 | 接口 | 描述 |
|------|------|------|
| `queryuser` | SAMR | 检索用户信息 |
| `querygroup` | | 检索组信息 |
| `querydominfo` | | 检索域信息 |
| `enumdomusers` | | 枚举域用户 |
| `enumdomgroups` | | 枚举域组 |
| `createdomuser` | | 创建域用户 |
| `deletedomuser` | | 删除域用户 |
| `lookupnames` | LSARPC | 将用户名查找为安全标识符 SID 值 |
| `lookupsids` | | 将 SID 查找为用户名（相对标识符 RID 循环） |
| `lsaaddacctrights` | | 向用户账户添加权限 |
| `lsaremoveacctrights` | | 从用户账户移除权限 |
| `dsroledominfo` | LSARPC-DS | 获取主域信息 |
| `dsenumdomtrusts` | | 枚举 AD 林中的受信任域 |

工具
- `rpcclient` 命名管道 RPC 交互
    - `lookupsids` 循环枚举用户：
        - 获取已知账户的 SID 值
        - 递增 RID 值以枚举其他用户

    - `enumdomusers` 命令通过 SAMR 列出用户

- `walksam` 实用程序查询 SAMR 服务以收集用户信息
    - 在通过 `rpcdump` 或类似实用程序找到 SAMR 接口后，使用正确的序列（例如 TCP、UDP 或命名管道）执行定向查询

像 `walksam` 这样的枚举工具使用 RID 循环来列出用户（通过查找 RID 500、501、502 等），并识别本地管理员账户，即使它已被重命名。