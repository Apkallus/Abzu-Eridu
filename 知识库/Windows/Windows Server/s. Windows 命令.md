https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/windows-commands

# Windows 命令

## chcp

更改活动控制台代码页。 如果不带参数使用，那么 `chcp` 将显示活动控制台代码页的编号。

```powershell
chcp [<nnn>]
```

- `<nnn>` 	
    指定代码页。

可用编号见[代码页标识符](https://learn.microsoft.com/zh-cn/windows/win32/intl/code-page-identifiers)
- `437` 	
    美国
- `65001`  
    utf-8
