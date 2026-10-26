# sudo —— 以其他用户的身份执行命令

[官网文档](https://www.sudo.ws/)
[linux 手册](https://man7.org/linux/man-pages/man8/sudo.8.html)

```sh
sudo -h | -K | -k | -V sudo -v [-ABkNnS] [-g group] [-h host] [-p
prompt] [-u user] sudo -l [-ABkNnS] [-g group] [-h host] [-p
prompt] [-U user] [-u user] [command [arg ...]] sudo [-ABbEHnPS]
[-C num] [-D directory] [-g group] [-h host] [-p prompt] [-R
directory] [-T timeout] [-u user] [VAR=value] [-i | -s] [command
[arg ...]] sudoedit [-ABkNnS] [-C num] [-D directory] [-g group]
[-h host] [-p prompt] [-R directory] [-T timeout] [-u user]
file ...
```

`sudo` 默认以 `root` 身份运行命令.  
`sudo` 通过检查策略来确定用户是否被授权以 `root` 身份运行命令。这些策略在 `/etc/sudoers` 文件中定义（似乎此文件本身即需要 root 权限读取）

参数
- `-u 用户名` 切换到用户后运行
- `-l, --list`

	- 如果未指定命令，则列出调用用户（或由 `-U` 选项指定的用户）在当前主机上的权限。若指定 `-ll`，且安全策略支持详细输出格式，则会采用更长的列表格式。

	- 如果指定了命令，且安全策略允许调用用户（或由 `-U` 选项指定的用户）在当前主机上执行该命令，则会显示该命令的完全限定路径及其所有参数。若指定 `-ll`（且安全策略支持），则会以详细格式显示匹配规则以及该命令。如果指定了命令但策略不允许，`sudo` 将以状态值 1 退出。


示例
```sh
sudo bash -c "多条命令"
```
- sudo 后执行一条命令，若尝试执行复杂操作，最简单的是开启子进程 shell
