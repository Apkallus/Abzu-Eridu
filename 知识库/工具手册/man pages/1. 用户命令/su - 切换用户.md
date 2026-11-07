https://www.man7.org/linux/man-pages/man1/su.1.html

# `su` - 使用替代用户和组 ID 运行命令

## 概要

```sh
su [options] [-] [user|UID [argument...]]
```

## 描述

`su` 允许使用替代用户和组 ID 运行命令。

当未指定 `user` 调用时，`su` 默认以 `root` 身份运行交互式 shell。当指定 `user` 时，可以提供额外的 `argument`，在这种情况下它们会被传递给 shell。

为了向后兼容，`su` 默认不更改当前目录，并且仅设置环境变量 `HOME` 和 `SHELL`（如果目标 `user` 不是 `root`，还会设置 `USER` 和 `LOGNAME`）。建议始终使用 `--login` 选项（而不是其快捷方式 `-`），以避免混合环境造成的副作用。

此版本的 `su` 使用 PAM 进行身份验证、帐户和会话管理。其他 `su` 实现中的某些配置选项（例如对 `wheel` 组的支持）必须通过 PAM 配置。

`su` 主要面向非特权用户设计；对于特权用户（例如由 `root` 执行的脚本），推荐的解决方案是使用非 set-user-ID 命令 [runuser(1)]，它不需要身份验证并提供单独的 PAM 配置。如果完全不需要 PAM 会话，则推荐的解决方案是使用命令 [setpriv(1)]。

注意，在所有情况下，`su` 都使用 PAM（[pam_getenvlist(3)]）进行最终环境修改。诸如 `--login` 和 `--preserve-environment` 等命令行选项会在 PAM 修改环境之前影响环境。

自 2.38 版本起，`su` 重置进程资源限制 `RLIMIT_NICE`、`RLIMIT_RTPRIO`、`RLIMIT_FSIZE`、`RLIMIT_AS` 和 `RLIMIT_NOFILE`。

## 选项

- `-c`, `--command` `command`  
  通过 `-c` 选项将 `command` 传递给 shell。通过 [setsid(2)] 创建新会话。若要保持同一会话，请参考 `--session-command`。

- `-f`, `--fast`  
  将 `-f` 传递给 shell，是否有用取决于 shell。

- `-g`, `--group` `group`  
  指定主组。此选项仅对 `root` 用户可用。

- `-G`, `--supp-group` `group`  
  指定补充组。此选项仅对 `root` 用户可用。如果未指定 `--group` 选项，则第一个指定的补充组也用作主组。

- `-`, `-l`, `--login`  
  以登录 shell 启动 shell，环境类似于真实登录。  
    
  注意，在基于 [systemd(1)] 的系统上，新会话可能被定义为系统的真实入口点。然而，从这一角度看，`su` 不会（通过 PAM）创建真实会话。你需要使用 [systemd-run(1)] 或 [machinectl(1)] 等工具来启动完整、真实的会话。  
    
  `su` 会执行以下操作：  
    
    - 清除所有环境变量，但 `TERM`、`COLORTERM`、`NO_COLOR` 以及由 `--whitelist-environment` 指定的变量除外  
    - 初始化环境变量 `HOME`、`SHELL`、`USER`、`LOGNAME` 和 `PATH`  
    - 切换到目标用户的主目录  
    - 将 shell 的 `argv[0]` 设置为 `-`，以使 shell 成为登录 shell

- `-m`, `-p`, `--preserve-environment`  
  保留整个环境，即不设置 `HOME`、`SHELL`、`USER` 或 `LOGNAME`。如果指定了 `--login` 选项，则忽略此选项。

- `-P`, `--pty`  
  为会话创建伪终端。独立终端提供更好的安全性，因为用户不与原始会话共享终端。请注意下面关于 `TIOCSTI` 漏洞的安全建议。  
    
  整个会话也可以移到后台（例如 `su --pty - user -c application &`）。如果启用伪终端，则 `su` 充当会话之间的代理（同步 `stdin` 和 `stdout`）。  
    
  此功能主要面向交互式会话设计。如果标准输入不是终端，而是例如管道（如 `echo "date" | su --pty`），则伪终端的 `ECHO` 标志被禁用，以避免输出混乱。

- `-s`, `--shell` `shell`  
  运行指定的 `shell` 而不是默认 shell。如果目标用户具有受限 shell（即未列在 `/etc/shells` 中），则除非调用用户是 `root`，否则忽略 `--shell` 选项和 `SHELL` 环境变量。  
    
  要运行的 shell 按以下规则依次选择：  
    
    - 使用 `--shell` 指定的 shell  
    - 如果使用了 `--preserve-environment` 选项，则使用环境变量 `SHELL` 中指定的 shell  
    - 目标用户 `passwd` 条目中列出的 shell  
    - `/bin/sh`

- `--session-command=` `command`  
  与 `-c` 相同，但不创建新会话。（不推荐。）请注意下面关于 `TIOCSTI` 漏洞的安全建议。

- `-T`, `--no-pty`  
  不创建伪终端，与 `--pty` 和 `-P` 相反。请注意下面关于 `TIOCSTI` 漏洞的安全建议。

- `-w`, `--whitelist-environment` `list`  
  在为 `--login` 清除环境时，不重置逗号分隔的 `list` 中指定的环境变量。白名单对 `HOME`、`SHELL`、`USER`、`LOGNAME` 和 `PATH` 环境变量被忽略。

- `-h`, `--help`  
  显示帮助文本并退出。

- `-V`, `--version`  
  显示版本并退出。

## 信号

收到 `SIGINT`、`SIGQUIT` 或 `SIGTERM` 时，`su` 终止其子进程，然后以收到的信号终止自身。子进程先被 `SIGTERM` 终止；如果尝试失败并延迟 2 秒后，子进程被 `SIGKILL` 杀死。

## 配置文件

`su` 读取 `/etc/default/su` 和 `/etc/login.defs` 配置文件。以下配置项与 `su` 相关：

- `FAIL_DELAY`（数字）  
  身份验证失败时的延迟秒数。该数字必须是非负整数。

- `ENV_PATH`（字符串）  
  为普通用户定义 `PATH` 环境变量。默认值为 `/usr/local/bin:/bin:/usr/bin`。

- `ENV_ROOTPATH`（字符串）、`ENV_SUPATH`（字符串）  
  为 `root` 定义 `PATH` 环境变量。`ENV_SUPATH` 优先。默认值为 `/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`。

- `ALWAYS_SET_PATH`（布尔值）  
  如果设置为 `yes`，且未指定 `--login` 和 `--preserve-environment`，则 `su` 初始化 `PATH`。  
    
  在 `/bin` 和 `/sbin` 合并到 `/usr` 的系统上，环境变量 `PATH` 可能不同；此变量还受 `--login` 命令行选项和 PAM 系统设置（例如 [pam_env(8)]）影响。

## 退出状态

`su` 通常返回其执行命令的退出状态。如果命令被信号杀死，`su` 返回信号编号加 `128`。

`su` 自身生成的退出状态：

- `1`  
  执行请求命令前的通用错误

- `126`  
  请求的命令无法执行

- `127`  
  未找到请求的命令

## 环境

- `SU_DEBUG=all`  
  启用 `su` 调试输出。

- `ULPTY_DEBUG=all`  
  启用 pty 调试输出。

## 文件

- `/etc/pam.d/su`  
  默认 PAM 配置文件

- `/etc/pam.d/su-l`  
  如果指定 `--login`，则使用此 PAM 配置文件

- `/etc/default/su`  
  命令特定的 logindef 配置文件

- `/etc/login.defs`  
  全局 logindef 配置文件

## 安全说明

如果 `su` 与原始会话共享终端，则可能通过 `TIOCSTI`/`TIOCLINUX` `ioctl` 命令注入而容易受到权限提升攻击。有两种内置方法可以防止这种情况：可以使用带 `-c` 选项的 `su`，它会通过 [setsid(2)] 启动一个新会话，且没有控制终端。或者，如果你的用例需要控制终端（例如交互式会话），可以指示 `su` 使用伪终端，使用 `--pty` 或 `-P` 选项。

出于安全原因，`su` 始终将失败的登录尝试记录到 `btmp` 文件，但完全不写入 `lastlog` 文件。可以通过 PAM 配置使用此解决方案控制 `su` 行为。如果你想使用 [pam_lastlog(8)] 模块打印有关失败登录尝试的警告消息，则必须将 [pam_lastlog(8)] 配置为同时更新 `lastlog` 文件。例如：

```text
session required pam_lastlog.so nowtmp
```

## 历史

此 `su` 命令源自 coreutils 的 `su`，后者基于 David MacKenzie 的实现。util-linux 版本由 Karel Zak 重构。

## 另请参阅

[setpriv(1)]、[login.defs(5)]、[shells(5)]、[pam(8)]、[runuser(1)]

## 报告缺陷

如需报告缺陷，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`su` 命令是 util-linux 软件包的一部分，可从 Linux 内核归档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 *util-linux*（Linux 实用工具的随机集合）项目的一部分。项目信息可在 <https://www.kernel.org/pub/linux/utils/util-linux/> 找到。若对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页取自该项目上游 Git 仓库 <git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-08-03。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`util-linux 2.43.devel-739-eee2e` · 2026-05-24 · `SU(1)`