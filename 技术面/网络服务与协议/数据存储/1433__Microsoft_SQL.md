
## Microsoft SQL Server

概念：
- 运行Microsoft SQL Server的主机通常暴露两个端口：
    * TCP端口1433，客户端用于与服务及数据库交互
    * UDP端口1434，提供解析服务（列出可用实例）

- 服务器可以使用各种高端口运行多个数据库实例。监听UDP端口1434的SQL Server解析服务（SSRS）提供解析——列出已注册的SQL Server实例及其传输详细信息（例如TCP端口和命名管道）。

工具：
- Nmap在遇到SQL Server接口时会调用`ms-sql-info`脚本，该脚本通过UDP端口1434查询SRSS接口并检索可用数据库实例的详细信息。

将SQL Server版本与NVD交叉引用以识别弱点。

### 暴力破解密码

Microsoft SQL Server下的默认管理帐户是`sa`。其他有时会创建的帐户包括`distributor_admin`、`sql`、`sqluser`、`sql_account`、`sql_user`和`sql-user`。

工具：
- TCP/IP（1433）进行暴力破解密码
    - Hydra
    - Metasploit `mssql_login` 模块
- 使用命名管道通过SMB进行暴力破解
    - `sqlbf`[^9]

[^9]: 参见 [http://examples.oreilly.com/networksa/tools/sqlbf.zip](http://examples.oreilly.com/networksa/tools/sqlbf.zip)。

### 认证与配置评估

工具：
- Metasploit模块，将这些模块与有效凭证结合使用，以在SQL Server实例上执行命令和获取数据。
- Patrik Karlsson的SQLAT工具包还支持通过扩展存储过程进行文件上传、注册表访问和SAM数据库下载。


### 后渗透

`xp_cmdshell` 的管理级存储过程。在 SQL 中，存储过程是可重用的代码段，而 `xp_cmdshell` 允许在 SQL 服务器服务使用的相同安全上下文下执行操作系统命令。使用的 MS SQL 版本默认禁用了此存储过程，但如果在 MS SQL 中具有 `sysadmin` 角色，则可以使用 SQL 命令重新启用它。

将首先运行一个查询来帮助识别具有 `sysadmin` 权限的用户帐户。运行以下查询以查看具有此级别访问权限的所有用户，然后成为这些用户之一：

```sql
SELECT name, type_desc, is_disabled FROM master.sys.server_principals
WHERE IS_SRVROLEMEMBER ('sysadmin', name) = 1
```

如果具有 `sysadmin` 角色，几乎可以保证完全破坏系统。在 MS SQL 查询窗口中运行以下命令以启用 `xp_cmdshell` 存储过程：

```sql
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
xp_cmdshell "ipconfig";
```

将 `sp_configure` 标志设置为 1，以便可以看到高级选项。然后，运行 `RECONFIGURE` 命令，以便的更改生效，并运行 `EXEC sp_configure` 以显示所有配置。设置 `xp_cmdshell` 标志，并再次使用 `RECONFIGURE` 命令应用配置。

最后，为了确保的更改成功，使用 `xp_cmdshell` 存储过程在操作系统上执行命令。在此示例中，执行 `ipconfig` 操作系统命令。
