# `credentials` — 进程标识符

https://man7.org/linux/man-pages/man7/credentials.7.html

## 描述

### 进程 ID（PID）

每个进程都有一个唯一的非负整数标识符，在进程通过 [fork(2)] 创建时分配。进程可以使用 [getpid(2)] 获取其 PID。PID 使用类型 `pid_t`（定义在 `<sys/types.h>` 中）表示。

PID 在一系列系统调用中用于标识受调用影响的进程，例如：[kill(2)]、[ptrace(2)]、[setpriority(2)]、[setpgid(2)]、[setsid(2)]、[sigqueue(3)] 和 [waitpid(2)]。

进程的 PID 在 [execve(2)] 期间保持不变。

### 父进程 ID（PPID）

进程的父进程 ID 标识使用 [fork(2)] 创建该进程的进程。进程可以使用 [getppid(2)] 获取其 PPID。PPID 使用类型 `pid_t` 表示。

进程的 PPID 在 [execve(2)] 期间保持不变。

### 进程组 ID 和会话 ID

每个进程都有一个会话 ID 和一个进程组 ID，二者均使用类型 `pid_t` 表示。进程可以使用 [getsid(2)] 获取其会话 ID，使用 [getpgrp(2)] 获取其进程组 ID。

由 [fork(2)] 创建的子进程继承其父进程的会话 ID 和进程组 ID。进程的会话 ID 和进程组 ID 在 [execve(2)] 期间保持不变。

会话和进程组是为支持 shell 作业控制而设计的抽象。进程组（有时称为“作业”）是共享同一进程组 ID 的进程集合；shell 为用于执行单个命令或管道的进程创建一个新的进程组（例如，为执行命令 `ls | wc` 而创建的两个进程被放入同一进程组）。可以使用 [setpgid(2)] 设置进程的组成员关系。进程 ID 与其进程组 ID 相同的进程是该组的*进程组组长*。

会话是共享同一会话 ID 的进程集合。进程组的所有成员也具有相同的会话 ID（即，进程组的所有成员始终属于同一会话，因此会话和进程组形成严格的进程两级层次结构）。当进程调用 [setsid(2)] 时创建新会话，这会创建一个新会话，其会话 ID 与调用 [setsid(2)] 的进程的 PID 相同。会话的创建者称为*会话首进程*。

会话中的所有进程共享一个*控制终端*。控制终端在会话首进程首次打开终端时建立（除非调用 [open(2)] 时指定了 `O_NOCTTY` 标志）。一个终端至多可以是一个会话的控制终端。

会话中至多有一个作业可以是*前台作业*；会话中的其他作业是*后台作业*。只有前台作业可以从终端读取；当后台进程尝试从终端读取时，其进程组会收到 `SIGTTIN` 信号，从而挂起该作业。如果已为终端设置 `TOSTOP` 标志（见 [termios(3type)]），则只有前台作业可以写入终端；来自后台作业的写入会产生 `SIGTTOU` 信号，从而挂起该作业。当按下产生信号的终端按键（例如*中断*键，通常是 `control-C`）时，信号会发送到前台作业中的进程。

各种系统调用和库函数可以作用于进程组的所有成员，包括 [kill(2)]、[killpg(3)]、[getpriority(2)]、[setpriority(2)]、[ioprio_get(2)]、[ioprio_set(2)]、[waitid(2)] 和 [waitpid(2)]。另请参见 [fcntl(2)] 中关于 `F_GETOWN`、`F_GETOWN_EX`、`F_SETOWN` 和 `F_SETOWN_EX` 操作的讨论。

### 用户和组标识符

每个进程都有各种关联的用户和组 ID。这些 ID 是整数，分别使用类型 `uid_t` 和 `gid_t`（定义在 `<sys/types.h>` 中）表示。

在 Linux 上，每个进程具有以下用户和组标识符：

- 真实用户 ID 和真实组 ID。  
  这些 ID 决定谁拥有该进程。进程可以使用 [getuid(2)]（[getgid(2)]）获取其真实用户（组）ID。

- 有效用户 ID 和有效组 ID。  
  内核使用这些 ID 确定进程在访问消息队列、共享内存和信号量等共享资源时将具有的权限。在大多数 UNIX 系统上，这些 ID 还决定访问文件时的权限。然而，Linux 使用下面描述的文件系统 ID 来完成此任务。进程可以使用 [geteuid(2)]（[getegid(2)]）获取其有效用户（组）ID。

- 保存的设置用户 ID 和保存的设置组 ID。  
  这些 ID 在 `set-user-ID` 和 `set-group-ID` 程序中使用，用于保存程序执行时设置的相应有效 ID 的副本（见 [execve(2)]）。`set-user-ID` 程序可以通过在真实用户 ID 和保存的设置用户 ID 中的值之间来回切换其有效用户 ID 来假定和放弃特权。此切换通过调用 [seteuid(2)]、[setreuid(2)] 或 [setresuid(2)] 完成。`set-group-ID` 程序使用 [setegid(2)]、[setregid(2)] 或 [setresgid(2)] 执行类似任务。进程可以使用 [getresuid(2)]（[getresgid(2)]）获取其保存的设置用户 ID（设置组 ID）。

- 文件系统用户 ID 和文件系统组 ID（Linux 特有）。  
  这些 ID 与下面描述的补充组 ID 一起用于确定访问文件的权限；详情见 [path_resolution(7)]。每当进程的有效用户（组）ID 更改时，内核也会自动将文件系统用户（组）ID 更改为相同的值。因此，文件系统 ID 通常与相应的有效 ID 具有相同的值，因此 Linux 上文件权限检查的语义与其他 UNIX 系统相同。可以通过调用 [setfsuid(2)] 和 [setfsgid(2)] 使文件系统 ID 与有效 ID 不同。

- 补充组 ID。  
  这是一组附加的组 ID，用于访问文件和其他共享资源时的权限检查。在 Linux 2.6.4 之前，一个进程最多可以属于 32 个补充组；自 Linux 2.6.4 起，一个进程最多可以属于 65536 个补充组。可以使用调用 `sysconf(_SC_NGROUPS_MAX)` 确定进程可以属于的补充组数量。进程可以使用 [getgroups(2)] 获取其补充组 ID 集合。

由 [fork(2)] 创建的子进程继承其父进程用户和组 ID 的副本。在 [execve(2)] 期间，进程的真实用户和组 ID 以及补充组 ID 保持不变；有效 ID 和保存的设置 ID 可能会更改，如 [execve(2)] 所述。

除上述用途外，进程的用户 ID 还用于许多其他上下文：

- 确定发送信号的权限时（见 [kill(2)]）；
- 使用 [setpriority(2)]、[sched_setaffinity(2)]、[sched_setscheduler(2)]、[sched_setparam(2)]、[sched_setattr(2)] 和 [ioprio_set(2)] 确定设置进程调度参数（`nice` 值、实时调度策略和优先级、CPU 亲和性、I/O 优先级）的权限时；
- 检查资源限制时（见 [getrlimit(2)]）；
- 检查进程可以创建的 `inotify` 实例数量限制时（见 [inotify(7)]）。

### 修改进程用户和组 ID

在相关手册页描述的规则约束下，进程可以使用以下 API 修改其用户和组 ID：

- [setuid(2)]（[setgid(2)]）  
  修改进程的真实（可能还有有效和保存设置）用户（组）ID。

- [seteuid(2)]（[setegid(2)]）  
  修改进程的有效用户（组）ID。

- [setfsuid(2)]（[setfsgid(2)]）  
  修改进程的文件系统用户（组）ID。

- [setreuid(2)]（[setregid(2)]）  
  修改进程的真实和有效（可能还有保存设置）用户（组）ID。

- [setresuid(2)]（[setresgid(2)]）  
  修改进程的真实、有效和保存设置用户（组）ID。

- [setgroups(2)]  
  修改进程的补充组列表。

对进程有效用户（组）ID 的任何更改都会自动传递到进程的文件系统用户（组）ID。对进程有效用户或组 ID 的更改还可能影响进程的 `dumpable` 属性，如 [prctl(2)] 所述。

对进程用户和组 ID 的更改可能影响进程的能力，如 [capabilities(7)] 所述。

## 标准

进程 ID、父进程 ID、进程组 ID 和会话 ID 在 POSIX.1 中规定。真实、有效和保存的设置用户和组 ID，以及补充组 ID，在 POSIX.1 中规定。

文件系统用户和组 ID 是 Linux 扩展。

## 注释

`/proc/pid/status` 文件中的各种字段显示上述进程凭据。更多信息见 [proc(5)]。

POSIX 线程规范要求进程中的所有线程共享凭据。然而，在内核层面，Linux 为每个线程维护单独的用户和组凭据。`NPTL` 线程实现会做一些工作，以确保对用户或组凭据的任何更改（例如调用 [setuid(2)]、[setresuid(2)]）都传递到进程中的所有 POSIX 线程。更多详情见 [nptl(7)]。

## 另请参见

[bash(1)]、[csh(1)]、[groups(1)]、[id(1)]、[newgrp(1)]、[ps(1)]、[runuser(1)]、[setpriv(1)]、[sg(1)]、[su(1)]、[access(2)]、[execve(2)]、[faccessat(2)]、[fork(2)]、[getgroups(2)]、[getpgrp(2)]、[getpid(2)]、[getppid(2)]、[getsid(2)]、[kill(2)]、[setegid(2)]、[seteuid(2)]、[setfsgid(2)]、[setfsuid(2)]、[setgid(2)]、[setgroups(2)]、[setpgid(2)]、[setresgid(2)]、[setresuid(2)]、[setsid(2)]、[setuid(2)]、[waitpid(2)]、[euidaccess(3)]、[initgroups(3)]、[killpg(3)]、[tcgetpgrp(3)]、[tcgetsid(3)]、[tcsetpgrp(3)]、[group(5)]、[passwd(5)]、[shadow(5)]、[capabilities(7)]、[namespaces(7)]、[path_resolution(7)]、[pid_namespaces(7)]、[pthreads(7)]、[signal(7)]、[system_data_types(7)]、[unix(7)]、[user_namespaces(7)]、[sudo(8)]

## 版权说明

本页面是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。有关该项目的信息可在 <https://www.kernel.org/doc/man-pages/> 找到。如果您对本手册页有错误报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页面取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 man-pages-6.19.tar.gz 压缩包。如果您发现此 HTML 版本页面存在渲染问题，或者您认为有更好或更新的页面来源，或者您对本版权说明（*不*属于原始手册页的一部分）中的信息有更正或改进，请发送邮件至 `man-pages@man7.org`。

Linux man-pages 6.19 2026-07-02 `credentials`(7)