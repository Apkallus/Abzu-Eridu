# `passwd` - 密码文件

https://man7.org/linux/man-pages/man5/passwd.5.html

## 描述

`/etc/passwd` 文件是一个文本文件，用于描述系统的用户登录账户。它应对所有用户允许读权限（许多工具，如 [`ls(1)`] 用它把用户 ID 映射到用户名），但只对超级用户允许写权限。

在过去的美好年代，这种全局读权限并没有大问题。每个人都能读取加密密码，但硬件太慢，无法破解一个精心选择的密码，而且当时的基本假设是友好的用户社区。如今，许多人运行某种版本的影子密码套件，其中 `/etc/passwd` 的密码字段中有一个 `x` 字符，而加密密码位于 `/etc/shadow` 中，该文件仅超级用户可读。

如果加密密码（无论在 `/etc/passwd` 还是 `/etc/shadow` 中）是空字符串，则允许登录，甚至无需询问密码。注意，此功能可能在应用程序中被有意禁用，或可配置（例如使用 [`pam_unix(8)`] 的 `"nullok"` 或 `"nonull"` 参数）。

如果 `/etc/passwd` 中的加密密码是 `*NP*`（不带引号），则应从 NIS+ 服务器获取影子记录。

无论是否使用影子密码，许多系统管理员都会在加密密码字段中使用星号（`*`），以确保该用户无法使用密码进行身份验证。（但请参见下文“注释”。）

如果你创建新的登录账户，请先在密码字段中放入星号（`*`），然后使用 [`passwd(1)`] 设置密码。

文件的每一行描述单个用户，并包含七个以冒号分隔的字段：

```text
name:password:UID:GID:GECOS:directory:shell
```

各字段如下：

- `name`  
  这是用户的登录名。它不应包含大写字母。

- `password`  
  这可以是加密的用户密码、星号（`*`）或字母 `x`。（关于 `x` 的说明，参见 [`pwconv(8)`]。）

- `UID`  
  特权 `root` 登录账户（超级用户）的用户 ID 为 `0`。

- `GID`  
  这是该用户的数字主组 ID。（用户的附加组在系统组文件中定义；参见 [`group(5)`]。）

- `GECOS`  
  此字段（有时称为“注释字段”）是可选的，仅用于信息目的。通常，它包含完整用户名。某些程序（例如 `finger(1)`）会显示此字段的信息。  
  GECOS 代表“General Electric Comprehensive Operating System”，当 GE 的大型系统部门被出售给 Honeywell 时，它被重命名为 GCOS。Dennis Ritchie 曾报告：“有时我们会把打印机输出或批处理作业发送到 GCOS 机器。密码文件中的 gcos 字段是存放 $IDENTcard 信息的地方。并不优雅。”

- `directory`  
  这是用户的主目录：用户登录后最初所在的目录。此字段的值用于设置 `HOME` 环境变量。

- `shell`  
  这是登录时运行的程序（如果为空，则使用 `/bin/sh`）。如果设置为不存在的可执行文件，用户将无法通过 [`login(1)`] 登录。此字段的值用于设置 `SHELL` 环境变量。

## 文件

`/etc/passwd`

## 注释

如果你想创建用户组，`/etc/group` 中必须有对应条目，否则该组将不存在。

如果加密密码设置为星号（`*`），用户将无法使用 [`login(1)`] 登录，但仍可能使用 `rlogin(1)` 登录、运行现有进程并通过 `rsh(1)`、[`cron(8)`]、`at(1)` 或邮件过滤器等启动新进程。尝试仅通过更改 shell 字段来锁定账户会产生相同结果，并且还允许使用 [`su(1)`]。

## 另见

[`chfn(1)`], [`chsh(1)`], [`login(1)`], [`passwd(1)`], [`su(1)`], [`crypt(3)`], [`getpwent(3)`], [`getpwnam(3)`], [`group(5)`], [`shadow(5)`], [`vipw(8)`]

## 版本信息

本页是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/doc/man-pages/>⟩ 找到。如果你对本手册页有错误报告，请参见 ⟨<https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>⟩。本页取自 2026-09-09 从 ⟨<https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/>⟩ 获取的 man-pages-6.19.tar.gz tarball。如果你发现此 HTML 版本页面中的渲染问题，或认为有更好或更新的页面来源，或对 COLOPHON 中的信息（其 *不是* 原始手册页的一部分）有更正或改进，请发送邮件至 man-pages@man7.org。

```text
Linux man-pages 6.19            2025-09-21                      passwd(5)
```