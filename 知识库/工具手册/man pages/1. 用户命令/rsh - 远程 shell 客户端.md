https://man.archlinux.org/man/rsh.1.en

# `rsh` - 远程 shell 客户端

## 概要

```sh
rsh [OPTION...] [USER@]HOST [COMMAND [ARG...]]
```

## 描述

远程 shell

- `-4`, `--ipv4`  
    仅使用 IPv4

- `-6`, `--ipv6`  
    仅使用 IPv6

- `-8`, `--8-bit`  
    始终允许八位输入数据路径

- `-d`, `--debug`  
    开启套接字调试（参见 `setsockopt(2)`）

- `-e`, `--escape=CHAR`  
    允许用户指定转义字符（默认为 `~`）

- `-l`, `--user=USER`  
    在远程系统上以 `USER` 身份运行

- `-n`, `--no-input`  
    使用 `/dev/null` 作为输入

- `-?`, `--help`  
    显示此帮助列表

- `--usage`  
    显示简短用法消息

- `-V`, `--version`  
    打印程序版本

长选项的强制或可选参数对于任何对应的短选项也是强制或可选的。

## 作者

由许多作者编写。

## 报告缺陷

将缺陷报告发送至 <bug-inetutils@gnu.org>。

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 GPLv3+：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。
这是自由软件：您可以自由更改和重新分发它。在法律允许的范围内，不提供任何保证。

## 另请参见

`rshd(1)`

`rsh` 的完整文档作为 Texinfo 手册维护。如果 `info` 和 `rsh` 程序在您的站点上正确安装，命令

```sh
info rsh
```

应能让您访问完整手册。