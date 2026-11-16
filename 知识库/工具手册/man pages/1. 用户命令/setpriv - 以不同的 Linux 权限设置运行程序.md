https://man7.org/linux/man-pages/man1/setpriv.1.html

# `setpriv` - 以不同的 Linux 权限设置运行程序

## 概要

```sh
setpriv [options] program [arguments]
```

## 描述

设置或查询各种跨 `execve(2)` 继承的 Linux 权限设置。

与 `su(1)` 和 `runuser(1)` 相比，`setpriv` 既不使用 PAM，也不提示输入密码。它是对 `execve(2)` 的简单、非 set-user-ID 包装器，可用于以与 **daemontools** 的 `setuidgid(8)`、**runit** 的 `chpst(8)` 或其他服务管理器附带的类似工具相同的方式降低权限。

## 选项

- `--clear-groups`  
    清除补充组。

- `-d`, `--dump`  
    转储当前权限状态。此选项可以多次指定，以显示额外的、大多无用的信息。与其他所有选项不兼容。

- `--groups group...`  
    设置补充组。参数是以逗号分隔的 GID 或名称列表。

- `--inh-caps (+|-)cap...`, `--ambient-caps (+|-)cap...`, `--bounding-set (+|-)cap...`  
    设置可继承能力、环境能力或能力边界集。参见 `capabilities(7)`。参数是以逗号分隔的 `+cap` 和 `-cap` 条目列表，分别添加或移除一个条目。`cap` 可以是 `capabilities(7)` 中所见的、不带 `cap_` 前缀的人类可读名称，也可以是 `cap_N` 格式，其中 `N` 是 Linux 使用的内部能力索引。可以使用 `+all` 和 `-all` 添加或移除所有能力。

    对于 `--inh-caps`，能力集初始为当前可继承集；对于 `--ambient-caps`，初始为当前环境集；对于 `--bounding-set`，初始为当前边界集。

    请注意以下关于修改这些能力集的限制（详见 `capabilities(7)`）：

    - 只有当某能力当前存在于边界集中时，才能将其添加到可继承集。
    - 只有当某能力当前同时存在于允许集和可继承集中时，才能将其添加到环境集。
    - 尽管 `setpriv` 提供了相应语法，但内核不允许将能力添加到边界集。

    如果你从边界集中删除某项能力而未同时从可继承集中删除它，你很可能会感到困惑。不要这样做。

- `--keep-groups`  
    保留补充组。仅与 `--rgid`、`--egid` 或 `--regid` 一起使用时有用。

- `--init-groups`  
    使用 `initgroups3` 初始化补充组。仅与 `--ruid` 或 `--reuid` 一起使用时有用。

- `--list-caps`  
    列出所有已知能力。此选项必须单独指定。

- `--nnp`, `--no-new-privs`  
    设置 *no_new_privs* 位。设置此位后，`execve(2)` 不会授予新权限。例如，set-user-ID 和 set-group-ID 位以及文件能力将被禁用。（执行设置了这些位的二进制文件仍可工作，但它们不会获得权限。某些 LSM，尤其是 AppArmor，可能导致某些程序执行失败。）此位由子进程继承且无法取消设置。参见 `prctl(2)` 以及 Linux 内核源码中的 `Documentation/prctl/no_new_privs.txt`。

    *no_new_privs* 位自 Linux 3.5 起受支持。

- `--rgid gid`, `--egid gid`, `--regid gid`  
    设置实际、有效或两者的 GID。`gid` 参数可以作为文本组名给出。

    为安全起见，如果设置任何主 `gid`，你必须指定 `--clear-groups`、`--groups`、`--keep-groups` 或 `--init-groups` 之一。

- `--ruid uid`, `--euid uid`, `--reuid uid`  
    设置实际、有效或两者的 UID。`uid` 参数可以作为文本登录名给出。

    设置 `uid` 或 `gid` 不会更改能力，尽管最后的 exec 调用可能会更改能力。这意味着，如果你是 root，你可能想执行类似以下操作：

    ```sh
    setpriv --reuid=1000 --regid=1000 --inh-caps=-all
    ```

- `--securebits (+|-)securebit...`  
    设置或清除 securebits。参数是以逗号分隔的列表。有效的 securebits 有：

    - `noroot`
    - `noroot_locked`
    - `no_setuid_fixup`
    - `no_setuid_fixup_locked`
    - `keep_caps_locked`（`keep_caps` 会被 `execve(2)` 清除，因此不允许）
    - `no_cap_ambient_raise`
    - `no_cap_ambient_raise_locked`
    - `exec_restrict_file`
    - `exec_restrict_file_locked`
    - `exec_deny_interactive`
    - `exec_deny_interactive_locked`

- `--pdeathsig keep|clear|<signal>`  
    保留、清除或设置父进程死亡信号。某些 LSM（最显著的是 SELinux 和 AppArmor）会在进程凭据更改时清除该信号。使用 `--pdeathsig keep` 将在更改凭据后恢复父进程死亡信号，以补救该情况。

- `--ptracer pid|any|none`  
    当 Yama 的受限 ptrace 模式生效时（即 `/proc/sys/kernel/yama/ptrace_scope` 设置为 1），允许由具有指定 PID 的进程、任何进程或无进程通过 `ptrace(2)` 跟踪。参见 `PR_SET_PTRACER(2const)`。（注意，这不会被子进程继承，但会跨 `execve(2)` 保留。）当 Yama 未启用或处于受限 ptrace 以外的模式时，此选项无效。

- `--selinux-label label`  
    请求特定的 SELinux 转换（使用 exec 上的转换，而非 dyntrans）。如果未使用 SELinux，这将失败并导致 `setpriv` 中止，并且转换可能被忽略或导致 `execve(2)` 按 SELinux 的意愿失败。（特别是，这不太可能与 *no_new_privs* 一起工作。）这类似于 `runcon(1)`。

- `--apparmor-profile profile`  
    请求特定的 AppArmor 配置文件（使用 exec 上的转换）。如果未使用 AppArmor，这将失败并导致 `setpriv` 中止，并且转换可能被忽略或导致 `execve(2)` 按 AppArmor 的意愿失败。

- `--landlock-access access`  
    为特定的一组系统访问启用 landlock 限制。要允许特定的访问子组，请使用 `--landlock-rule`。

    阻止所有文件系统访问：

    ```sh
    setpriv --landlock-access fs
    ```

    阻止所有文件删除和目录创建：

    ```sh
    setpriv --landlock-access fs:remove-file,make-dir
    ```

    关于支持的完整访问类别集，请使用 `setpriv --help`。

    通用占位符 "fs" 可能会更改，并可能在未来的版本中扩展以支持新的访问类型。

- `--landlock-rule rule`  
    允许 `--landlock-access` 所阻止类别中的一项特定访问。

    语法如下：

    ```sh
    --landlock-rule $ruletype:$access:$rulearg
    ```

    例如，授予对 `/boot` 下所有内容的文件读取访问权限：

    ```sh
    --landlock-rule path-beneath:read-file:/boot
    ```

- `--seccomp-filter file`  
    从文件加载原始 BPF seccomp 过滤器代码。

    例如，可以使用 `enosys` 创建过滤器。

- `--reset-env`
    - 清除所有环境变量，但 `TERM` 环境变量除外
    - 根据用户的 passwd 条目初始化环境变量 `HOME`、`SHELL`、`USER`、`LOGNAME`
    - 如果用户的 passwd 条目中未给出，则环境变量 `SHELL` 默认为 `/bin/sh`。
    - 根据 `/etc/login.defs` 中的设置（`ENV_PATH`、`ENV_SUPATH` 或 `ENV_ROOTPATH` 变量）重置 `PATH` 环境变量，或者对于普通用户默认为 `/usr/local/bin:/bin:/usr/bin`，对于 root 默认为 `/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`。

        在 `/bin` 和 `/sbin` 合并到 `/usr` 的系统上，环境变量 `PATH` 可能不同。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-V`, `--version`  
    显示版本并退出。

## 注意事项

如果应用任何指定选项失败，则不会运行 `program`，`setpriv` 将以退出状态 127 返回。

使用此工具时要小心——它可能会产生意外的安全后果。例如，设置 *no_new_privs* 然后执行一个受 SELinux 限制的程序（如此工具所做的那样）可能会阻止 SELinux 限制生效。

## 示例

请注意，`setpriv` 不是 `su(1)`、`runuser(1)` 或 `sudo(8)` 的 1:1 替代品。与这些工具不同，`setpriv` 不使用 PAM、不提示输入密码，也不执行会话或记账设置。以下示例为常见的降低权限场景提供了起点。

如果你想以类似于 `runuser(1)` 的方式（不使用 `--login`）切换 UID/GID，请尝试：

```sh
setpriv --reuid=1000 --regid=1000 --inh-caps=-all --init-groups
```

还要重置环境（如 `sudo(8)` 默认所做的那样），请添加 `--reset-env`：

```sh
setpriv --reuid=1000 --regid=1000 --inh-caps=-all --init-groups
--reset-env
```

对于更严格的设置，同时还限制边界集并防止获得新权限（比 `runuser` 或 `sudo` 更严格）：

```sh
setpriv --reuid=1000 --regid=1000 --init-groups --inh-caps=-all
--bounding-set=-all --no-new-privs --reset-env
```

如果你想模仿 daemontools 的 `setuid(8)`，请尝试：

```sh
setpriv --reuid=1000 --regid=1000 --clear-groups
```

## 作者

Andy Lutomirski <luto@amacapital.net>

## 另请参见

“runuser(1)”、“su(1)”、“prctl(2)”、“capabilities(7)”、“landlock(7)”

## 报告缺陷

关于缺陷报告，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`setpriv` 命令是 util-linux 包的一部分，可从 Linux 内核存档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 `util-linux`（一个 Linux 实用程序的随机集合）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页获取自项目上游 Git 仓库 ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
util-linux 2.43.devel-1062-f... 2026-08-03                     SETPRIV(1)
```