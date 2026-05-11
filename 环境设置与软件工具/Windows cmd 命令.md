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