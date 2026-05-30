# Unix RPC 服务

概念：
- 许多 Unix 守护进程（例如 NIS 和 NFS 组件）通过动态高端口暴露 RPC 服务。为了跟踪注册的端点并向客户端提供可用 RPC 服务的列表，端口映射服务监听在 TCP 和 UDP 端口 111（以及 Oracle Solaris 中的端口 32771）。

指纹识别：
- Nmap 
- 手动
    - `rsysinfo`
    - `showmount` 揭示了导出的 NFS 目录（以及关联的 ACL）
        - 对权限较弱的目录用 `mount` 命令访问
    - 获取环境的 NIS 域名后，使用 `ypwhich` 命令 ping NIS 服务器
        - 使用 `ypcat` 使用映射文件获取敏感材料

攻击面：
- 在遗留环境中，许多服务容易受到远程攻击。IANA 还维护着一个全面的 RPC 程序编号、描述和参考列表[^78]。

[^78]: 参见 IANA.org 上的“Remote Procedure Call (RPC) Program Numbers”。


NFS、NIS 和 NIS+ 是配置和测试起来相当复杂的系统，因此如果在实际环境中遇到它们，请考虑阅读 Mike Eisler、Ricardo Labiaga 和 Hal Stern 的《Managing NFS and NIS》第二版（O‘Reilly，2001），该书详细介绍了这些协议的最内部工作原理。

**常见的 NIS 映射和对应的文件**

| 主文件 | 映射 | 说明 |
|--------|------|------|
| `/etc/hosts` | `hosts.byname`, `hosts.byaddr` | 包含主机名和 IP 详细信息 |
| `/etc/passwd` | `passwd.byname`, `passwd.byuid` | NIS 用户密码文件 |
| `/etc/group` | `group.byname`, `group.bygid` | NIS 组文件 |
| `/usr/lib/aliases` | `mail.aliases` | 邮件别名详情 |

## RPC rusers

商业 Unix 平台（包括 Oracle Solaris、HP-UX 和 IBM AIX）通常暴露一个 RPC `rusersd` 端点，该端点揭示活动的用户会话。

工具
- `rusers` 客户端用于检索材料
