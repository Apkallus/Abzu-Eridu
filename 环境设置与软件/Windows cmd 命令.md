https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/windows-commands

使用左侧边栏搜索命令

## cmd - 启动命令解释器的新实例，cmd.exe

如果未使用参数， cmd 则显示作系统的版本和版权信息。

```cmd
cmd [/c|/k] [/s] [/q] [/d] [/a|/u] [/t:{<b><f> | <f>}] [/e:{on | off}] [/f:{on | off}] [/v:{on | off}] [<string>]
```

- `/c`	执行由 `<string>` 命令处理器指定的命令，然后退出命令处理器。

## type - 显示文本文件的内容

在 PowerShell 中， type 是 Get-Content cmdlet 的内置别名，该 cmdlet 也显示文件的内容，但使用不同的语法。

```cmd
type [<drive>:][<path>]<filename>
```

## findstr - 搜索文件中的文本模式。

```cmd
findstr [/b] [/e] [/l | /r] [/s] [/i] [/x] [/v] [/n] [/m] [/o] [/p] [/f:<file>] [/c:<string>] [/g:<file>] [/d:<dirlist>] [/a:<colorattribute>] [/off[line]] <strings> [<drive>:][<path>]<filename>[ ...]
```

## Network shell (netsh) - 网络配置工具

https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh

命令上下文
- `advfirewall` [高级防火墙](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-advfirewall)
  - `set` 更新设置
    - `allprofiles` 设置所有配置文件中的属性
    - `state` 配置防火墙状态
    - `on/off` 开启/关闭防火墙

  `netsh advfirewall set allprofiles state off`

## net user - 添加、修改或删除用户帐户，并显示有关本地计算机或域上用户帐户的详细信息

https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-user

```ps
net user [<UserName> {<Password> | *} [<Options>]] [/domain]
net user [<UserName> {<Password> | *} /add [<Options>] [/domain]]
net user [<UserName> [/delete] [/domain]]
net user username [/times:{times | all}]
net user username [/active: {yes | no}]
```

例
- `net user apkallus 12345678 /add`

## Net localgroup - 添加、显示或修改本地组

如果不带参数使用，**net localgroup** 会显示服务器名称以及计算机上本地组的名称。

**Net localgroup** 是内置于 Windows Vista 的命令行工具。若要运行 **net localgroup**，请打开命令提示符，输入带相应参数的 **net localgroup**，然后按 Enter 键。

```text
net localgroup [<GroupName> [/comment:"<Text>"]] [/domain]
net localgroup [<GroupName> {/add [/comment:"<Text>"] | /delete} [/domain]
net localgroup [<GroupName> <Name> […] {/add |  /delete} [/domain]
```

参数
- **<GroupName>**  
  指定要添加、展开或删除的本地组的名称。如果不带其他参数使用，**net localgroup <GroupName>** 会显示本地组中的用户或全局组列表。

- **/comment:"<Text>"**  
  为新组或现有组添加注释。注释最多可包含 256 个字符。请将文本括在引号中。

- **/domain**  
  在当前域的主域控制器上执行操作。否则，操作会在本地计算机上执行。

- **<Name> [ ...]**  
  列出一个或多个要添加到本地组或从本地组中删除的用户名或组名。

- **/add**  
  将全局组名或用户名添加到本地组中。在使用此命令将用户或全局组添加到本地组之前，必须先为其建立帐户。

- **/delete**  
  从本地组中删除组名或用户名。

- **net help <Command>**  
  显示指定的 **net** 命令的帮助。

## Runas - 允许用户使用与当前登录所提供的权限不同的权限来运行特定工具和程序。

**Runas** 是一个内置的命令行工具。要在命令行中使用 **runas**，请打开命令提示符，输入带有相应参数的 **runas**，然后按 Enter 键。

在用户界面中，“**运行方式…**”命令已更改为“**以管理员身份运行**”。但是，您应该很少需要使用“以管理员身份运行”命令，因为 Windows Vista 会在需要时自动提示您输入管理员密码。

`runas [{/profile | /noprofile}] [/env] [{/netonly | /savecred}] [/smartcard] [/showtrustlevels] [/trustlevel] /user:<UserAccountName> "<ProgramName> <PathToProgramFile>"`

atips：
- 需交互式 shell，而 meterpreter 不满足

## Netstat - 网络状态

- `-a`	显示所有活动的 TCP 连接数以及计算机正在侦听的 TCP 和 UDP 端口。

- `-n`	显示活动的 TCP 连接数，但是，地址和端口号以数字表示，并且不会尝试确定名称。

- `-o`	显示活动的 TCP 连接数，并包括每个连接的进程 ID (PID)。 可以在 Windows 任务管理器的“进程”选项卡上基于 PID 找到应用程序。 

例
- `netstat -ano`

atips
- `-n` 选项显示数字而不解析名称，从而大幅提高查询速度