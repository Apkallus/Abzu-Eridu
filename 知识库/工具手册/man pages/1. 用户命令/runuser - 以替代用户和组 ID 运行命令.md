https://man7.org/linux/man-pages/man1/runuser.1.html

# `runuser` - 以替代用户和组 ID 运行命令

## 概要

```sh
runuser [options] -u user [[--] command [argument...]]

runuser [options] [-] [user [argument...]]
```

## 描述

`runuser` 可用于以替代用户和组 ID 运行命令。如果未给出 `-u` 选项，`runuser` 回退到与 `su` 兼容的语义并执行 shell。`runuser` 与 `su` 命令的区别在于 `runuser` 不询问密码（因为它只能由 root 用户执行），并且使用不同的 PAM 配置。`runuser` 命令不必以 set-user-ID 权限安装。

如果不需要 PAM 会话，则推荐的解决方案是使用“setpriv(1)”命令。

不带参数调用时，`runuser` 默认以 `root` 身份运行交互式 shell。

为向后兼容，`runuser` 默认不更改当前目录，并且仅设置环境变量 `HOME` 和 `SHELL`（如果目标 `user` 不是 root，还设置 `USER` 和 `LOGNAME`）。此版本的 `runuser` 使用 PAM 进行会话管理。

请注意，在所有情况下，`runuser` 都使用 PAM（`pam_getenvlist(3)`）进行最终的环境修改。诸如 `--login` 和 `--preserve-environment` 之类的命令行选项会在 PAM 修改环境之前影响环境。

自版本 2.38 起，`runuser` 重置进程资源限制 `RLIMIT_NICE`、`RLIMIT_RTPRIO`、`RLIMIT_FSIZE`、`RLIMIT_AS` 和 `RLIMIT_NOFILE`。

## 选项

- `-c`, `--command=command`  
    使用 `-c` 选项将 `command` 传递给 shell。通过 `setsid(2)` 创建新会话。若要保留同一会话，请参考 `--session-command`。

- `-f`, `--fast`  
    将 `-f` 传递给 shell，这可能有用也可能没用，取决于 shell。

- `-g`, `--group=group`  
    要使用的主组。此选项仅允许 root 用户使用。

- `-G`, `--supp-group=group`  
    指定补充组。此选项仅对 root 用户可用。如果未指定 `--group` 选项，则第一个指定的补充组也用作主组。

- `-`, `-l`, `--login`  
    以登录 shell 启动 shell，环境类似于真实登录：

    - 清除所有环境变量，但 `TERM`、`COLORTERM`、`NO_COLOR` 以及由 `--whitelist-environment` 指定的变量除外
    - 初始化环境变量 `HOME`、`SHELL`、`USER`、`LOGNAME` 和 `PATH`
    - 切换到目标用户的主目录
    - 将 shell 的 `argv[0]` 设置为 `-` 以使 shell 成为登录 shell

- `-m`, `-p`, `--preserve-environment`  
    保留整个环境，即不设置 `HOME`、`SHELL`、`USER` 或 `LOGNAME`。如果指定了 `--login` 选项，则忽略此选项。

- `-P`, `--pty`  
    为会话创建伪终端。独立终端提供更好的安全性，因为用户不与原始会话共享终端。请注意下文关于 TIOCSTI 漏洞的安全建议。

    整个会话也可以移到后台（例如 `runuser --pty -u user -- command &`）。如果启用了伪终端，则 `runuser` 作为会话之间的代理（同步 stdin 和 stdout）。

    此功能主要设计用于交互式会话。如果标准输入不是终端，而是例如管道（例如 `echo "date" | runuser --pty -u user`），则禁用伪终端的 `ECHO` 标志以避免混乱的输出。

- `-s`, `--shell=shell`  
    运行指定的 `shell` 而不是默认值。要运行的 shell 按以下顺序规则选择：

    - 使用 `--shell` 指定的 shell
    - 如果使用了 `--preserve-environment` 选项，则为环境变量 `SHELL` 中指定的 shell
    - 目标用户 passwd 条目中列出的 shell
    - `/bin/sh`

    如果目标用户具有受限 shell（即未列在 `/etc/shells` 中），则除非调用用户是 root，否则忽略 `--shell` 选项和 `SHELL` 环境变量。

- `--session-command=command`  
    与 `-c` 相同，但不创建新会话。（不推荐。）请注意下文关于 TIOCSTI 漏洞的安全建议。

- `-T`, `--no-pty`  
    不创建伪终端，与 `--pty` 和 `-P` 相反。请注意下文关于 TIOCSTI 漏洞的安全建议。

- `-u`, `--user=user`  
    以用户名 `user` 的有效用户 ID 和组 ID 运行 `command`。

- `-w`, `--whitelist-environment=list`  
    在为 `--login` 清除环境时，不重置逗号分隔的 `list` 中指定的环境变量。白名单对 `HOME`、`SHELL`、`USER`、`LOGNAME` 和 `PATH` 环境变量会被忽略。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-V`, `--version`  
    显示版本并退出。

## 配置文件

`runuser` 读取 `/etc/default/runuser` 和 `/etc/login.defs` 配置文件。以下配置项与 `runuser` 相关：

- `ENV_PATH`（字符串）  
    为普通用户定义 `PATH` 环境变量。默认值为 `/usr/local/bin:/bin:/usr/bin`。

- `ENV_ROOTPATH`（字符串）、`ENV_SUPATH`（字符串）  
    为 root 定义 `PATH` 环境变量。`ENV_SUPATH` 优先。默认值为 `/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`。

- `ALWAYS_SET_PATH`（布尔值）  
    如果设置为 `yes` 且未指定 `--login` 和 `--preserve-environment`，`runuser` 会初始化 `PATH`。

在 `/bin` 和 `/sbin` 合并到 `/usr` 的系统上，环境变量 `PATH` 可能不同；此变量还受 `--login` 命令行选项和 PAM 系统设置（例如 `pam_env(8)`）的影响。

## 退出状态

`runuser` 通常返回其执行命令的退出状态。如果命令被信号杀死，`runuser` 返回信号编号加 128。

`runuser` 本身生成的退出状态：

- `1`  
    执行请求的命令之前的通用错误

- `126`  
    无法执行请求的命令

- `127`  
    未找到请求的命令

## 环境

- `SU_DEBUG=all`  
    启用 su 调试输出。

- `ULPTY_DEBUG=all`  
    启用 pty 调试输出。

## 文件

- `/etc/pam.d/runuser`  
    默认 PAM 配置文件

- `/etc/pam.d/runuser-l`  
    如果指定了 `--login`，则为 PAM 配置文件

- `/etc/default/runuser`  
    runuser 特定的 logindef 配置文件

- `/etc/login.defs`  
    全局 logindef 配置文件

## 安全注意事项

如果 `runuser` 与原始会话共享终端，则可能容易受到通过 TIOCSTI/TIOCLINUX ioctl 命令注入的权限提升攻击。有两种内置方法可以防止这种情况：你可以使用带 `-c` 选项的 `runuser`，它通过 `setsid(2)` 启动没有控制终端的新会话。或者，如果你的用例需要控制终端（例如交互式会话），你可以指示 `runuser` 使用 `--pty` 或 `-P` 选项的伪终端。

## 历史

此 `runuser` 命令源自 coreutils 的 `su`（其基于 David MacKenzie 的实现）以及 Dan Walsh 编写的 Fedora `runuser` 命令。

## 另请参见

“setpriv(1)”、“su(1)”、“login.defs(5)”、“shells(5)”、“pam(8)”

## 报告缺陷

关于缺陷报告，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`runuser` 命令是 util-linux 包的一部分，可从 Linux 内核存档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 `util-linux`（一个 Linux 实用程序的随机集合）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页获取自项目上游 Git 仓库 ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
util-linux 2.43.devel-739-eee2e 2026-05-24                     RUNUSER(1)
```