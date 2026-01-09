在过去，典型的 Linux 系统会设置一个 `root` 密码，管理员在用自己的普通账户密码登录后，会通过 `su` 命令切换至 `root` 身份。但维护 `root` 密码十分麻烦，它们（或其哈希值！）可能泄漏，且难以适应大规模环境（例如服务器集群）。为解决这一问题，近几十年来，业界已从通过 `su` 进行管理转向通过 `sudo` 进行管理（*有趣的事实*：`sudo` 最初代表 **su**peruser **do**，后演变为 "`su` 'do'"，由于 `su` 意为 "substitute user"，`sudo` 的当前含义是 "substitute user, do"）。

与默认以指定用户身份启动 shell 的 `su` 不同，`sudo` 默认以 `root` 身份运行命令：
```sh
hacker@dojo:~$ whoami
hacker
hacker@dojo:~$ sudo whoami
root
hacker@dojo:~$
```

或更贴近获取 flag 的场景：
```sh
hacker@dojo:~$ grep hacker /etc/shadow
grep: /etc/shadow: Permission denied
hacker@dojo:~$ sudo grep hacker /etc/shadow
hacker:$6$Xro.e7qB3Q2Jl2sA$j6xffIgWn9xIxWUeFzvwPf.nOH2NTWNJCU5XVkPuONjIC7jL467SR4bXjpVJx4b/bkbl7kyhNquWtkNlulFoy.:19921:0:99999:7:::
hacker@dojo:~$
```


与依赖密码认证的 `su` 不同，`sudo` 通过检查策略来确定用户是否被授权以 `root` 身份运行命令。这些策略在 `/etc/sudoers` 文件中定义，尽管这超出我们当前讨论范围，但有许多[资源](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)可供学习！

因此，世界已转向使用 `sudo`，并（就系统管理而言）将 `su` 抛在身后。事实上，甚至 pwn.college 的 Privileged Mode 也是通过授予您 `sudo` 访问权限来实现特权提升！

在本关卡中，我们将为您提供 `sudo` 访问权限，您需要用它来读取 flag。简单又轻松！

______________________________________________________________________

**注意：**
本关卡结束后，我们将启用 Privileged Mode！当您以 Privileged Mode 启动挑战时（通过点击 `Privileged` 按钮而非 `Start` 按钮），生成的容器将授予您完整的 `sudo` 访问权限，以便您尽情进行内省和调试，但当然只会提供占位符 flag。
