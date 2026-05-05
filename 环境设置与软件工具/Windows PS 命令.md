<https://learn.microsoft.com/zh-cn/powershell/scripting/>

使用左侧边栏搜索命令

## 目录文件操作

- `ls X:\`
    目录详情

- `cd X:\`
    进入目录

- `cp <from> <to>`
    复制


## 字符


- `Select-String` [查找字符串和文件中的文本。](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/select-string?view=powershell-7.6)
    - `[-Pattern] <String[]>`
    - `[-Path] <String[]>`
    - `[-Context <Int32[arg1,arg2]>]`
        捕获与模式匹配的行前后的指定行数。例如，`-Context 2,3`

- `Format-Hex` [将文件或其他输入显示为十六进制。](https://learn.microsoft.com/zh-cn/powershell/module/microsoft.powershell.utility/format-hex?view=powershell-7.6)
    - `[-Path] <String[]>`

## 进程 

- `Get-Process`
    获取在本地计算机上运行的进程。

    别名
    - 所有平台：`gps`
    - windows：`ps`
    
- `Stop-Process`
    停止一个或多个正在运行的进程。

    别名
    - 所有平台：`spps`
    - windows：`kill`

## 验证证书

- `Get-AuthenticodeSignature`
    得到验证签名对象
    - `.SignerCertificate`
        证书字段

- `Export-Certificate -Cert 证书对象.SignerCertificate -FilePath 保存路径`
    导出证书到路径

- `Import-Certificate -FilePath 证书路径 -CertStoreLocation Cert:\证书库`
    导入证书

- `Get-AuthenticodeSignature`
    查看验证签名信息

## 权限

- `Get-Acl`
    cmdlet 获取表示文件或资源的安全描述符的对象。 安全描述符包含资源的访问控制列表（ACL）。 ACL 指定用户和用户组有权访问资源的权限。