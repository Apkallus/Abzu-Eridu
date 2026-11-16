https://www.man7.org/linux/man-pages/man1/strace.1.html

## 名称

`strace` — 跟踪系统调用和信号

## 概要

```sh
strace [-ACdffhikkqqrtttTvVwxxyyYzZ] [-a column] [-b execve]
       [-e expr]... [-I n] [-o file] [-O overhead] [-p pid]...
       [-P path]... [-s strsize] [-S sortby] [-U columns]
       [-X format] [--seccomp-bpf]
       [--stack-trace-frame-limit=limit] [--syscall-limit=limit]
       [--secontext[=format]] [--tips[=format]] { -p pid | [-DDD]
       [-E var[=val]]... [-u username] command [args] }

strace -c [-dfwzZ] [-b execve] [-e expr]... [-I n] [-O overhead]
       [-p pid]... [-P path]... [-S sortby] [-U columns]
       [--seccomp-bpf] [--syscall-limit=limit] [--tips[=format]] {
       -p pid | [-DDD] [-E var[=val]]... [-u username] command
       [args] }

strace --tips[=format]
```

## 描述

在最简单的用法中，`strace` 运行指定的 `command` 直到其退出。它会拦截并记录进程发起的系统调用，以及进程接收到的信号。每个系统调用的名称、参数和返回值会打印到标准错误，或打印到由 `-o` 选项指定的文件。

`strace` 是一个有用的诊断、教学和调试工具。系统管理员、诊断人员与故障排查人员会发现，对于源代码不易获得的程序，它非常有价值，因为跟踪不需要重新编译。学生、黑客以及过度好奇的人会发现，即使跟踪普通程序，也能从系统及其系统调用中学到很多。程序员会发现，由于系统调用和信号发生在用户/内核接口处，仔细检查这个边界对于缺陷隔离、健全性检查以及尝试捕获竞态条件非常有用。

跟踪中的每一行包含系统调用名称，随后是括号中的参数及其返回值。跟踪命令 `cat /dev/null` 的一个示例是：

```log
open("/dev/null", O_RDONLY) = 3
```

错误通常由返回值 `-1` 表示，并会附加 `errno` 符号和错误字符串。

```log
open("/foo/bar", O_RDONLY) = -1 ENOENT (No such file or directory)
```

信号会以信号符号和解码后的 `siginfo` 结构打印。跟踪并中断命令 `sleep 666` 的片段是：

```log
sigsuspend([] <unfinished ...>
--- SIGINT {si_signo=SIGINT, si_code=SI_USER, si_pid=...} ---
+++ killed by SIGINT +++
```

如果一个系统调用正在执行时，另一个系统调用从不同线程或进程发起，`strace` 会尝试保留这些事件的顺序，并将正在进行的调用标记为 `unfinished`。当该调用返回时，它会被标记为 `resumed`。

```log
[pid 28772] select(4, [3], NULL, NULL, NULL <unfinished ...>
[pid 28779] clock_gettime(CLOCK_REALTIME, {tv_sec=1130322148, tv_nsec=3977000}) = 0
[pid 28772] <... select resumed> )      = 1 (in [3])
```

可重启系统调用因信号投递而被中断时，处理方式不同：内核会终止该系统调用，并安排在信号处理程序完成后立即重新执行它。

```log
read(0, 0x7ffff72cf5cf, 1)              = ? ERESTARTSYS (To be restarted)
--- SIGALRM {si_signo=SIGALRM, si_code=SI_KERNEL} ---
rt_sigreturn({mask=[]})                 = 0
read(0, "", 1)                          = 0
```

参数会尽可能以符号形式打印。下面的示例展示了 shell 执行 `>>xyzzy` 输出重定向：

```log
open("xyzzy", O_WRONLY|O_APPEND|O_CREAT, 0666) = 3
```

这里，`open(2)` 的第二个和第三个参数被解码：标志参数被拆解为三个按位或的组成部分，模式值则按传统以八进制打印。当传统或本地用法与 ANSI 或 POSIX 不同时，优先采用后者形式。某些情况下，`strace` 输出甚至比源码本身更易读。

结构体指针会被解引用，其成员会按需显示。大多数情况下，参数会以尽可能接近 C 语言的方式格式化。例如，命令 `ls -l /dev/null` 的核心内容被捕获为：

```log
lstat("/dev/null", {st_mode=S_IFCHR|0666, st_rdev=makedev(0x1, 0x3), ...}) = 0
```

注意 `struct stat` 参数如何被解引用，以及每个成员如何以符号形式显示。尤其要注意，`st_mode` 成员被仔细解码为符号值和数值的按位或。还要注意，在此示例中，`lstat(2)` 的第一个参数是系统调用的输入，第二个参数是输出。由于系统调用失败时输出参数不会被修改，因此参数不一定总会被解引用。例如，用不存在的文件重试 `ls -l` 示例会产生如下行：

```log
lstat("/foo/bar", 0xb004) = -1 ENOENT (No such file or directory)
```

在这种情况下，门廊灯亮着，但屋里没人。指针的值会被显示，因为它指向的结构体由于错误而未被填充。

`strace` 不认识的系统调用会以原始格式打印，十六进制系统调用号前会加上 `syscall_`：

```log
syscall_0xbad(0x1, 0x2, 0x3, 0x4, 0x5, 0x6) = -1 ENOSYS (Function not implemented)
```

字符指针会被解引用并打印为 C 字符串。字符串中的非打印字符通常用标准 C 转义码表示。只打印字符串的前 `strsize` 字节（默认 32）；更长的字符串会在结束引号后附加省略号。下面是 `ls -l` 中的一行，其中 `getpwuid(3)` 库例程正在读取密码文件：

```log
read(3, "root::0:0:System Administrator:/"..., 1024) = 422
```

结构体使用花括号标注，而基本类型指针和数组使用方括号打印，元素之间以逗号分隔。下面是系统具有补充组 ID 时命令 `id(1)` 的示例：

```log
getgroups(32, [100, 0]) = 2
```

另一方面，位集合也使用方括号显示，但集合元素之间仅以空格分隔。下面是 shell 准备执行外部命令时的示例：

```log
sigprocmask(SIG_BLOCK, [CHLD TTOU], []) = 0
```

这里，第二个参数是两个信号 `SIGCHLD` 和 `SIGTTOU` 的位集合。某些情况下，位集合非常满，打印未设置元素更有价值。此时，位集合前会加上波浪号，如下所示：

```log
sigprocmask(SIG_UNBLOCK, ~[], NULL) = 0
```

这里，第二个参数表示所有信号的完整集合。

## 选项

### 常规

- `-e expr`  
    通过指定限定表达式来修改要跟踪的事件或跟踪方式。表达式格式为：

    ```sh
    [qualifier=][!]value[,value]...
    ```

    其中 `qualifier` 是 `trace`（或 `t`）、`trace-fds`（或 `trace-fd`、`fd`、`fds`）、`abbrev`（或 `a`）、`verbose`（或 `v`）、`raw`（或 `x`）、`signal`（或 `signals`、`s`）、`read`（或 `reads`、`r`）、`write`（或 `writes`、`w`）、`fault`、`inject`、`status`、`quiet`（或 `silent`、`silence`、`q`）、`secontext`、`decode-fds`（或 `decode-fd`）、`decode-pids`（或 `decode-pid`）或 `kvm` 之一，`value` 是依赖于限定符的符号或数字。默认限定符是 `trace`。使用感叹号会否定值集合。例如，`-e open` 等价于 `-e trace=open`，意思是只跟踪 `open` 系统调用。相反，`-e trace=!open` 表示跟踪除 `open` 之外的每个系统调用。此外，特殊值 `all` 和 `none` 可分别用于跟踪每个事件或不跟踪任何事件。

    注意，某些 shell 即使在带引号的参数中也会使用感叹号进行历史扩展。在这种情况下，必须用反斜杠转义感叹号。

### 启动

- 
    ```
    -E var=val
    --env=var=val
    ```
    在执行命令时设置环境变量 `var=val`。

- 
    ```
    -E var
    --env=var
    ```
    在执行命令前从继承的环境变量中移除 `var`。

- 
    ```
    -p pid
    --attach=pid
    ```
    附加到进程 ID 为 `pid` 的进程并开始跟踪。跟踪可随时通过键盘中断信号（`CTRL-C`）终止。`strace` 会通过从被跟踪进程分离来响应，让它们继续运行。

    可以多次使用 `-p` 选项，以附加到多个进程；如果至少给出一个 `-p` 选项，则命令是可选的。

    单个 `-p` 选项可以接受多个进程 ID，彼此以逗号（“,”）、空格（“ ”）、制表符或换行符分隔。因此，支持 `-p "$(pidof PROG)"` 和 `-p "$(pgrep PROG)"` 这类语法。

- 
    ```
    -u username
    --user=username
    ```
    以 `username` 的用户 ID、组 ID 和补充组运行命令。此选项仅在以 root 运行时有用，因为它能正确执行 setuid 和/或 setgid 二进制程序。除非使用此选项，否则 setuid 和 setgid 程序会在没有其有效特权的情况下执行。

- 
    ```
    -u UID:GID
    --user=UID:GID
    ```
    另一种语法：程序以给定的用户 ID 和组 ID 启动，并使用空的补充组列表。此情况下不执行用户名和组名查找。

- `--argv0=name`  
    将所执行命令的 `argv[0]` 设置为 `name`。这对于跟踪会根据 `argv[0]` 解释自身行为的多调用可执行文件（例如 `busybox` 或 `kmod`）很有用。

### 跟踪

- 
    ```
    -b syscall
    --detach-on=syscall
    ```
    如果到达指定的系统调用，则从被跟踪进程分离。目前仅支持 `execve` 关键字，它包括 `execve(2)` 和 `execveat(2)` 系统调用。此选项对于使用 `-f` 跟踪多线程进程而不跟踪其（可能非常复杂的）子进程很有用。

- 
    ```
    -D
    --daemonize
    --daemonize=grandchild
    ```
    将跟踪器进程作为被跟踪进程的孙进程运行，而不是作为其父进程。这样可使被跟踪进程仍是调用进程的直接子进程，从而减少 `strace` 的可见影响。

- 
    ```
    -DD
    --daemonize=pgroup
    --daemonize=pgrp
    ```
    将跟踪器进程作为被跟踪进程的孙进程，在单独的进程组中运行。除了减少 `strace` 的可见影响外，这还可防止 `strace` 被发送到整个进程组的 `kill(2)` 信号终止。

- 
    ```
    -DDD
    --daemonize=session
    ```
    将跟踪器进程作为被跟踪进程的孙进程，在单独的会话中运行（即“真正的守护进程化”）。除了减少 `strace` 的可见影响外，这还可防止 `strace` 在会话终止时被终止。

- 
    ```
    -f
    --follow-forks
    ```
    跟踪当前被跟踪进程通过 `fork(2)`、`vfork(2)` 和 `clone(2)` 系统调用创建的子进程。注意，如果进程 `PID` 是多线程的，使用 `-f -p PID` 会附加到其所有线程，而不仅仅是 `thread_id = PID` 的那个线程。

- `--output-separately`  
    如果 `--output=filename` 选项生效，则每个进程的跟踪会写入单独的 `filename.pid` 文件，其中 `pid` 是进程 ID。

- 
    ```
    -ff
    --follow-forks --output-separately
    ```
    组合 `--follow-forks` 和 `--output-separately` 选项的效果。这与 `-c` 不兼容，因为不会保留每进程计数。

    使用 `strace-log-merge(1)` 可获得日志文件的合并视图。

- 
    ```
    -I interruptible
    --interruptible=interruptible
    ```
    控制 `strace` 何时可被信号（例如按 `CTRL-C`）中断。

    - `1`、`anywhere`  
        不阻塞任何信号。
    - `2`、`waiting`  
        在解码系统调用时阻塞致命信号（默认）。
    - `3`、`never`  
        始终阻塞致命信号（当使用 `-o FILE PROG` 时的默认值）。
    - `4`、`never_tstp`  
        始终阻塞致命信号和 `SIGTSTP`（`CTRL-Z`）（可用于让 `strace -o FILE PROG` 不在 `CTRL-Z` 时停止；使用 `-D` 时的默认值）。

- `--syscall-limit=limit`  
    在捕获 `limit` 个系统调用后分离所有被跟踪进程。通过 `--trace`、`--trace-path` 或 `--status` 选项过滤掉的系统调用不计入捕获的系统调用数量。

- `--kill-on-exit`  
    对所有被跟踪进程应用 `PTRACE_O_EXITKILL` ptrace 选项；如果跟踪器退出，则向被跟踪进程发送 `SIGKILL` 信号。这可防止跟踪器退出后被跟踪进程仍在运行，因为清理时不会分离它们。`--kill-on-exit` 与 `-p`/`--attach` 选项不兼容。

### 过滤

- 
    ```
    -e trace=syscall_set
    -e t=syscall_set
    --trace=syscall_set
    ```
    仅跟踪指定的系统调用集合。`syscall_set` 定义为 `[!]value[,value]`，`value` 可以是以下之一：

    - `syscall`  
        跟踪由名称指定的特定系统调用（参见 `syscalls(2)`，但也请参阅“注意”）。
    - `?value`  
        在限定前加问号可在未找到匹配系统调用时抑制错误。
    - `value@64`  
        将 `value` 描述的系统调用规格限制为 64 位 personality。
    - `value@32`  
        将 `value` 描述的系统调用规格限制为 32 位 personality。
    - `value@x32`  
        将 `value` 描述的系统调用规格限制为 x32 personality。
    - `all`  
        跟踪所有系统调用。
    - `/regex`  
        仅跟踪匹配 `regex` 的系统调用。可使用 POSIX 扩展正则表达式语法（参见 `regex(7)`）。
    - `%file`、`file`  
        跟踪所有以文件名为参数的系统调用。可以将其视为 `--trace=open,stat,chmod,unlink,...` 的缩写，这对于查看进程引用了哪些文件很有用。此外，使用该缩写可确保不会意外忘记包含 `newfstatat(2)` 之类的调用。不带前导百分号的语法（`--trace=file`）已弃用。
    - `%process`、`process`  
        跟踪与进程生命周期（创建、exec、终止）相关的系统调用。不带前导百分号的语法（`--trace=process`）已弃用。
    - `%net`、`%network`、`network`  
        跟踪所有与网络相关的系统调用。不带前导百分号的语法（`--trace=network`）已弃用。
    - `%signal`、`signal`  
        跟踪所有与信号相关的系统调用。不带前导百分号的语法（`--trace=signal`）已弃用。
    - `%ipc`、`ipc`  
        跟踪所有与 IPC 相关的系统调用。不带前导百分号的语法（`--trace=ipc`）已弃用。
    - `%desc`、`desc`  
        跟踪所有与文件描述符相关的系统调用。不带前导百分号的语法（`--trace=desc`）已弃用。
    - `%memory`、`memory`  
        跟踪所有与内存映射相关的系统调用。不带前导百分号的语法（`--trace=memory`）已弃用。
    - `%creds`  
        跟踪读取或修改用户和组标识符或能力集的系统调用。
    - `%stat`  
        跟踪 `stat` 系统调用变体。
    - `%lstat`  
        跟踪 `lstat` 系统调用变体。
    - `%fstat`  
        跟踪 `fstat`、`fstatat` 和 `statx` 系统调用变体。
    - `%%stat`  
        跟踪用于请求文件状态的系统调用（`stat`、`lstat`、`fstat`、`fstatat`、`statx` 及其变体）。
    - `%statfs`  
        跟踪 `statfs`、`statfs64`、`statvfs`、`osf_statfs` 和 `osf_statfs64` 系统调用。也可通过 `--trace=/^(.*_)?statv?fs` 正则表达式实现相同效果。
    - `%fstatfs`  
        跟踪 `fstatfs`、`fstatfs64`、`fstatvfs`、`osf_fstatfs` 和 `osf_fstatfs64` 系统调用。也可通过 `--trace=/fstatv?fs` 正则表达式实现相同效果。
    - `%%statfs`  
        跟踪与文件系统统计相关的系统调用（`statfs` 类、`fstatfs` 类和 `ustat`）。也可通过 `--trace=/statv?fs|fsstat|ustat` 正则表达式实现相同效果。
    - `%clock`  
        跟踪读取或修改系统时钟的系统调用。
    - `%pure`  
        跟踪总是成功且没有参数的系统调用。目前，此列表包括 `arc_gettls(2)`、`getdtablesize(2)`、`getegid(2)`、`getegid32(2)`、`geteuid(2)`、`geteuid32(2)`、`getgid(2)`、`getgid32(2)`、`getpagesize(2)`、`getpgrp(2)`、`getpid(2)`、`getppid(2)`、`get_thread_area(2)`（在非 x86 架构上）、`gettid(2)`、`get_tls(2)`、`getuid(2)`、`getuid32(2)`、`getxgid(2)`、`getxpid(2)`、`getxuid(2)`、`kern_features(2)` 和 `metag_get_tls(2)` 系统调用。

    `-c` 选项可用于确定哪些系统调用可能值得跟踪。例如，`--trace=open,close,read,write` 表示只跟踪这四个系统调用。如果只监视系统调用的一个子集，在推断用户/内核边界时要小心。默认值为 `--trace=all`。

- 
    ```
    -e trace-fd=set
    -e trace-fds=set
    -e fd=set
    -e fds=set
    --trace-fds=set
    ```
    仅跟踪对指定（非负）文件描述符子集进行操作的系统调用。注意，使用此选项还会过滤掉所有根本不操作文件描述符的系统调用。

    此过滤器与 `--trace-path` 过滤器组合；系统调用如果匹配其中任一过滤器，就会被跟踪。

- 
    ```
    -e signal=set
    -e signals=set
    -e s=set
    --signal=set
    ```
    仅跟踪指定的信号子集。默认值为 `--signal=all`。例如，`--signal=!SIGIO`（或 `--signal=!io`）会导致不跟踪 `SIGIO` 信号。

- 
    ```
    -e status=set
    --status=set
    ```
    仅打印具有指定返回状态的系统调用。默认值为 `--status=all`。使用 `status` 限定符时，事件的时序可能不会保留。这是因为 `strace` 必须等待系统调用完成才能决定是否打印它。如果两个系统调用由并发线程执行，`strace` 会先打印先退出的系统调用的进入和退出，而不管它们各自的进入时间。第二个退出的系统调用的进入和退出将在之后打印。下面是调用 `select(2)`，但另一个线程在 `select(2)` 完成前调用 `clock_gettime(2)` 的示例：

    ```log
    [pid 28779] 1130322148.939977 clock_gettime(CLOCK_REALTIME, {1130322148, 939977000}) = 0
    [pid 28772] 1130322148.438139 select(4, [3], NULL, NULL, NULL) = 1 (in [3])
    ```

    `set` 可包括以下元素：

    - `successful`  
        跟踪未返回错误码的系统调用。`-z` 选项的效果是 `--status=successful`。
    - `failed`  
        跟踪返回错误码的系统调用。`-Z` 选项的效果是 `--status=failed`。
    - `unfinished`  
        跟踪未返回的系统调用。例如，这可能由于同一线程组中不同线程的 `execve` 调用而发生。
    - `unavailable`  
        跟踪已返回但 `strace` 未能获取错误状态的系统调用。
    - `detached`  
        跟踪 `strace` 在返回前已分离的系统调用。

- 
    ```
    -P path
    --trace-path=path
    ```
    仅跟踪访问 `path` 的系统调用。可多次使用 `-P` 选项来指定多个路径。此过滤器与 `--trace-fds` 过滤器组合；系统调用如果匹配任一选项，就会被跟踪。

- 
    ```
    -z
    --successful-only
    ```
    仅打印未返回错误码的系统调用。

- 
    ```
    -Z
    --failed-only
    ```
    仅打印返回错误码的系统调用。

### 输出格式

- 
    ```
    -a column
    --columns=column
    ```
    将返回值对齐到指定列（默认列为 40）。

- 
    ```
    -e abbrev=syscall_set
    -e a=syscall_set
    --abbrev=syscall_set
    ```
    缩写大型结构体各成员的输出。`syscall_set` 规格的语法与 `--trace` 选项相同。默认值为 `--abbrev=all`。`-v` 选项的效果是 `--abbrev=none`。

- 
    ```
    -e verbose=syscall_set
    -e v=syscall_set
    --verbose=syscall_set
    ```
    对指定的系统调用集合解引用结构体。`syscall_set` 规格的语法与 `--trace` 选项相同。默认值为 `--verbose=all`。

- 
    ```
    -e raw=syscall_set
    -e x=syscall_set
    --raw=syscall_set
    ```
    对指定的系统调用集合打印原始、未解码的参数。`syscall_set` 规格的语法与 `--trace` 选项相同。此选项会使所有参数以十六进制打印。当不信任解码结果，或需要参数的实际数值时，此选项很有用。另请参阅 `-X raw` 选项。

- 
    ```
    -e read=set
    -e reads=set
    -e r=set
    --read=set
    ```
    对指定集合中列出的文件描述符读取到的所有数据执行完整的十六进制和 ASCII 转储。例如，要查看文件描述符 `3` 和 `5` 上的所有输入活动，使用 `--read=3,5`。注意，这与由 `--trace=read` 选项控制的 `read(2)` 系统调用的常规跟踪无关。

- 
    ```
    -e write=set
    -e writes=set
    -e w=set
    --write=set
    ```
    对指定集合中列出的文件描述符写入的所有数据执行完整的十六进制和 ASCII 转储。例如，要查看文件描述符 `3` 和 `5` 上的所有输出活动，使用 `--write=3,5`。注意，这与由 `--trace=write` 选项控制的 `write(2)` 系统调用的常规跟踪无关。

- 
    ```
    -e quiet=set
    -e silent=set
    -e silence=set
    -e q=set
    --quiet=set
    --silent=set
    --silence=set
    ```
    抑制各种信息消息。默认值为 `--quiet=none`。`set` 可包括以下元素：

    - `attach`  
        抑制关于附加和分离的消息（`[ Process NNNN attached ]`、`[ Process NNNN detached ]`）。
    - `exit`  
        抑制关于进程退出的消息（`+++ exited with SSS +++`）。
    - `path-resolution`  
        抑制关于通过 `-P` 选项提供的路径解析的消息（`Requested path "..." resolved into "..."`）。
    - `personality`  
        抑制关于进程 personality 变化的消息（`[ Process PID=NNNN runs in PPP mode. ]`）。
    - `thread-execve`、`superseded`  
        抑制关于进程被另一线程中的 `execve(2)` 取代的消息（`+++ superseded by execve in pid NNNN +++`）。

- 
    ```
    -e decode-fds=set
    --decode-fds=set
    ```
    解码与文件描述符相关的各种信息。默认值为 `--decode-fds=none`。`set` 可包括以下元素：

    - `path`  
        打印文件路径。还会在使用 `AT_FDCWD` 常量时启用打印被跟踪进程的当前工作目录。
    - `socket`  
        打印套接字协议特定信息。
    - `dev`  
        打印字符/块设备编号。
    - `eventfd`  
        打印与 eventfd 文件描述符关联的 eventfd 对象详情。
    - `pidfd`  
        打印与 pidfd 文件描述符关联的 PID。
    - `signalfd`  
        打印与 signalfd 文件描述符关联的信号掩码。

- 
    ```
    -e decode-pids=set
    --decode-pids=set
    ```
    解码与进程 ID（以及线程 ID、进程组 ID 和会话 ID）相关的各种信息。默认值为 `--decode-pids=none`。`set` 可包括以下元素：

    - `comm`  
        打印与线程或进程 ID 关联的命令名。
    - `pidns`  
        如果被跟踪进程位于不同的 PID 命名空间中，则按 `strace` 的 PID 命名空间打印线程、进程、进程组和会话 ID。

- 
    ```
    -e kvm=vcpu|vcpu+
    --kvm=vcpu|vcpu+
    ```
    打印 kvm vcpu 的退出原因（`vcpu`），或打印包含原因的整个 `kvm_run` 结构体（`vcpu+`）。需要 Linux 内核版本 4.16.0 或更高。

    `vcpu+` 输出使用前缀 `VCPU:CPU#<` 和 `VCPU:CPU#>`. 以前者开头的行表示调用 `KVM_RUN` 前的结构体状态，以后者开头的行表示调用 `KVM_RUN` 后的状态。

- 
    ```
    -e namespace=new
    --namespace=new
    ```
    打印被跟踪进程进入的新命名空间。支持以下系统调用：`clone(2)`、`clone3(2)`、`setns(2)` 和 `unshare(2)`。

- 
    ```
    -i
    --instruction-pointer
    ```
    打印系统调用时的指令指针。

- 
    ```
    -n
    --syscall-number
    ```
    打印系统调用号。

- 
    ```
    -N
    --arg-names
    ```
    打印系统调用参数名称。

- 
    ```
    -k
    --stack-trace[=symbol]
    ```
    在每次系统调用后打印被跟踪进程的执行栈回溯。

- 
    ```
    -kk
    --stack-trace=source
    ```
    在每次系统调用后打印被跟踪进程的执行栈回溯和源码信息。此选项要求目标程序使用适当的调试选项编译：`-g`（gcc）或 `-g -gdwarf-aranges`（clang）。

- `--stack-trace-frame-limit=limit`  
    回溯系统调用时，打印的栈回溯帧不超过此数量（默认 256）。请与 `--stack-trace`（或 `-k`）选项一起使用。

- 
    ```
    -o filename
    --output=filename
    ```
    将跟踪输出写入文件 `filename`，而不是写入标准错误。如果提供了 `-ff` 选项，则使用 `filename.pid` 形式。如果参数以 `|` 或 `!` 开头，则参数的其余部分被视为命令，所有输出会通过管道传给它。这对于在不影响所执行程序重定向的情况下将调试输出管道到程序很方便。当前，将输出管道到命令与 `-ff` 选项不兼容。

- 
    ```
    -A
    --output-append-mode
    ```
    以追加模式打开 `-o` 选项中提供的文件。

- `--color=when`  
    为跟踪输出着色。默认值为 `--color=auto`，仅当跟踪输出流是终端（默认是标准错误；参见 `-o`）且至少支持 8 色时才启用颜色。如果设置了 `NO_COLOR` 环境变量，除非指定 `--color=always`，否则禁用颜色。`when` 参数可以是 `auto`、`always` 或 `never` 之一。可使用 `STRACE_COLORS` 环境变量指定自定义配色方案，例如：

    ```sh
    STRACE_COLORS="syscall=1;33:argname=39:argval=35:call=1;34:const=1;36:comment=36:punct=0:retval=32:error=31"
    ```

    此值的格式是 `key=value` 对，以 `:` 分隔，值是以分号分隔的 SGR 码。

    默认调色板使用标准 ANSI 颜色（SGR 30–37）和粗体属性，而不是亮色（SGR 90–97），以便终端颜色主题可针对深色和浅色背景进行调整。

    可识别的颜色键为：`syscall`、`argname`、`argval`、`call`、`const`、`comment`、`punct`、`retval`、`error`。

- 
    ```
    -q
    --quiet
    --quiet=attach,personality
    ```
    抑制关于附加、分离和 personality 变化的消息。当输出重定向到文件且直接运行命令而不是附加时，会自动发生这种情况。

- 
    ```
    -qq
    --quiet=attach,personality,exit
    ```
    抑制关于附加、分离、personality 变化和进程退出状态的消息。

- 
    ```
    -qqq
    --quiet=all
    ```
    抑制所有可抑制的消息（请参阅 `--quiet` 选项描述以获取可抑制消息的完整列表）。

- 
    ```
    -r
    --relative-timestamps[=precision]
    ```
    在进入每个系统调用时打印相对时间戳。这会记录连续系统调用开始之间的时间差。`precision` 可以是 `s`（秒）、`ms`（毫秒）、`us`（微秒）或 `ns`（纳秒）之一，用于设置打印时间值的精度。默认值为 `us`（微秒）。注意，由于 `-r` 选项使用单调时钟，其测量值可能与使用墙上时钟的 `-t` 选项报告的时间差不同。

- 
    ```
    -s strsize
    --string-limit=strsize
    ```
    指定要打印的最大字符串大小（默认 32）。注意，文件名不被视为字符串，并且始终完整打印。

- 
    ```
    --absolute-timestamps[=[[format:]format],[[precision:]precision]]
    --timestamps[=[[format:]format],[[precision:]precision]]
    ```
    用指定 `format` 和指定 `precision` 的墙上时钟时间作为跟踪每一行的前缀。`format` 可以是以下之一：

    - `none`  
        不打印时间戳。可用于覆盖之前的设置。
    - `time`  
        墙上时钟时间（`strftime(3)` 格式字符串为 `%T`）。
    - `unix`  
        自 epoch 起的秒数（`strftime(3)` 格式字符串为 `%s`）。

    `precision` 可以是 `s`（秒）、`ms`（毫秒）、`us`（微秒）或 `ns`（纳秒）之一。该选项的默认参数为 `format:time,precision:s`。

- 
    ```
    -t
    --absolute-timestamps
    ```
    用墙上时钟时间作为跟踪每一行的前缀。

- 
    ```
    -tt
    --absolute-timestamps=precision:us
    ```
    以微秒精度打印墙上时钟时间。

- 
    ```
    -ttt
    --absolute-timestamps=format:unix,precision:us
    ```
    以微秒精度打印自 epoch 起的秒数形式的墙上时钟时间。

- 
    ```
    -T
    --syscall-times[=precision]
    ```
    显示在系统调用中花费的时间。这会记录每个系统调用开始和结束之间的时间差。`precision` 可以是 `s`（秒）、`ms`（毫秒）、`us`（微秒）或 `ns`（纳秒）之一，用于设置打印时间值的精度。默认值为 `us`（微秒）。

- 
    ```
    -v
    --no-abbrev
    ```
    打印环境、stat、termios 等调用的未缩写版本。这些结构体非常常见，因此默认行为是显示其成员的一个合理子集。使用此选项可查看所有成员的完整细节。

- `--strings-in-hex[=option]`  
    控制打印字符串时十六进制转义序列的使用。此选项会改变默认转义行为。

    通常（既未使用此选项也未使用 `-x` 时），`strace` 会在两种情况下引入转义序列：表示不可打印和非 ASCII 字符（即字符码小于 32 或大于 127 的字符），或消除输出歧义，例如转义括住字符串的引号或文件描述符路径中使用的尖括号。当字符必须转义时，如果存在符号化的 C 标准序列，`strace` 会优先使用：`\t`（制表符）、`\n`（换行）、`\v`（垂直制表符）、`\f`（换页）和 `\r`（回车）。对于所有其他需要转义的字符，`strace` 默认使用字符字节值的八进制表示。此选项允许覆盖此默认行为，使用十六进制转义而不是八进制。

    `option` 可以是以下之一：

    - `none`  
        输出中完全不使用十六进制数字。当需要发出转义序列时，使用八进制数字。
    - `non-ascii-chars`  
        在转义序列中使用十六进制数字而不是八进制。
    - `non-ascii`  
        包含非 ASCII 字符的字符串使用带十六进制数字的转义序列打印。
    - `all`  
        所有字符串都使用带十六进制数字的转义序列打印。

    当提供选项但未给参数时，假定为 `all`。

- 
    ```
    -x
    --strings-in-hex=non-ascii
    ```
    以十六进制字符串格式打印所有非 ASCII 字符串。

- 
    ```
    -xx
    --strings-in-hex[=all]
    ```
    以十六进制字符串格式打印所有字符串。

- 
    ```
    -X format
    --const-print-style=format
    ```
    设置命名常量和标志的打印格式。支持的 `format` 值为：

    - `raw`  
        原始数字输出，不解码。
    - `abbrev`  
        如果找到命名常量或标志集合，则输出它们而不是原始数字。这是 `strace` 的默认行为。
    - `verbose`  
        同时输出原始值和解码字符串（作为注释）。

- 
    ```
    -y
    --decode-fds
    --decode-fds=path
    ```
    打印与文件描述符参数以及 `AT_FDCWD` 常量关联的路径。

- 
    ```
    -yy
    --decode-fds=all
    ```
    打印与文件描述符关联的所有可用信息：与套接字文件描述符关联的协议特定信息、与设备文件描述符关联的块/字符设备编号，以及与 pidfd 文件描述符关联的 PID。

- 
    ```
    --pidns-translation
    --decode-pids=pidns
    ```
    如果 `strace` 和被跟踪进程位于不同的 PID 命名空间中，也按 `strace` 的命名空间打印 PID。

- 
    ```
    -Y
    --decode-pids=comm
    ```
    打印 PID 的命令名。

- 
    ```
    --secontext[=format]
    -e secontext=format
    ```
    当 SELinux 可用且未禁用时，在方括号中打印进程、文件和描述符的 SELinux 上下文。`format` 参数是逗号分隔的列表，其中每一项为以下之一：

    - `full`  
        打印完整上下文（用户、角色、类型、级别和类别）。
    - `mismatch`  
        如果当前上下文不同，还会打印 SELinux 数据库记录的上下文。后者会在两个感叹号（`!!`）后打印。

    `--secontext` 的默认值为 `!full,mismatch`，即仅打印类型而不是完整上下文，并且不检查上下文不匹配。

- `--always-show-pid`  
    对由 `strace` 启动的进程也显示 PID 前缀。当同时指定 `-f` 和 `-o` 时隐含启用。

### 统计

- 
    ```
    -c
    --summary-only
    ```
    统计每个系统调用的时间、调用次数和错误数，并在程序退出时报告摘要，同时抑制常规输出。这会显示系统时间（在内核中花费的 CPU 时间），它与墙上时钟时间无关。如果 `-c` 与 `-f` 一起使用，则只保留所有被跟踪进程的聚合总计。

- 
    ```
    -C
    --summary
    ```
    类似 `-c`，但在进程运行时也会打印常规输出。

- 
    ```
    -O overhead
    --summary-syscall-overhead=overhead
    ```
    将跟踪系统调用的开销设置为 `overhead`。这对于在使用 `-c` 选项计时系统调用时覆盖默认启发式估计很有用，该启发式会估计测量过程本身花费的时间。相同的开销会从多态时间列以及 `wall-total`、`wall-min`、`wall-max` 和 `wall-avg` 中减去。可通过在不跟踪的情况下（使用 `time(1)`）计时给定程序运行，并将累计系统调用时间与使用 `-c` 产生的总时间进行比较，来评估该启发式的准确性。

    `overhead` 规格的格式在“时间规格格式说明”一节中描述。

- 
    ```
    -S sortby
    --summary-sort-by=sortby
    ```
    按指定条件对 `-c` 选项打印的直方图输出进行排序。有效值为 `time`（或 `time-percent`、`time-total`、`total-time`）、`min-time`（或 `shortest`、`time-min`）、`max-time`（或 `longest`、`time-max`）、`avg-time`（或 `time-avg`）、`wall-total`（或 `total-wall`）、`wall-min`（或 `min-wall`）、`wall-max`（或 `max-wall`）、`wall-avg`（或 `avg-wall`）、`calls`（或 `count`）、`errors`（或 `error`）、`name`（或 `syscall`、`syscall-name`）以及 `nothing`（或 `none`）；默认值为 `time`。

- 
    ```
    -U columns
    --summary-columns=columns
    ```
    配置调用摘要中显示的列集合和顺序。`columns` 参数是逗号分隔的列表，包含以下一个或多个值：

    - `time-percent`（或 `time`）  
        特定系统调用消耗的累计时间百分比。
    - `total-time`（或 `time-total`）  
        特定系统调用消耗的总系统时间（如果提供 `-w` 选项，则为墙上时钟时间）。
    - `min-time`（或 `shortest`、`time-min`）  
        观察到的最小调用持续时间，以秒为单位。
    - `max-time`（或 `longest`、`time-max`）  
        观察到的最大调用持续时间，以秒为单位。
    - `avg-time`（或 `time-avg`）  
        每次调用的平均调用持续时间，以微秒为单位。
    - `wall-total`（或 `total-wall`）  
        特定系统调用消耗的总墙上时钟时间。无论 `-w` 选项如何，始终为墙上时钟时间，因此可在单次运行中与 `total-time` 一起显示。
    - `wall-min`（或 `min-wall`）  
        观察到的最小墙上时钟调用持续时间，以秒为单位。
    - `wall-max`（或 `max-wall`）  
        观察到的最大墙上时钟调用持续时间，以秒为单位。
    - `wall-avg`（或 `avg-wall`）  
        每次调用的平均墙上时钟调用持续时间，以微秒为单位。
    - `calls`（或 `count`）  
        调用次数。
    - `errors`（或 `error`）  
        错误次数。
    - `name`（或 `syscall`、`syscall-name`）  
        系统调用名称。

    默认值为 `time-percent,total-time,avg-time,calls,errors,name`。如果未显式提供 `name` 字段，则会将其添加为最后一列。

- 
    ```
    -w
    --summary-wall-clock
    ```
    汇总每个系统调用的墙上时钟时间，从其开始到结束测量。默认是汇总系统时间。

### 篡改

- `--inject=syscall_set[:error=errno|:retval=value][:signal=sig][:syscall=syscall][:delay_enter=delay][:delay_exit=delay][:poke_enter=@argN=DATAN,@argM=DATAM...][:poke_exit=@argN=DATAN,@argM=DATAM...][:when=expr]`  
    对指定的系统调用集合执行系统调用篡改。

    `syscall_set` 规格的语法与 `--trace` 选项相同。

    必须至少指定 `error`、`retval`、`signal`、`delay_enter`、`delay_exit`、`poke_enter` 或 `poke_exit` 动作选项之一。`error` 和 `retval` 互斥。

    如果指定 `error=errno` 选项，则会向系统调用注入故障。这是通过将系统调用号替换为 `-1`（表示无效系统调用）并将错误码设置为指定的 `errno` 来实现的。可使用 `syscall=` 选项覆盖将系统调用号替换为 `-1` 的行为。`errno` 可以是符号名（如 `ENOSYS`）或 1..4095 范围内的数值。

    如果指定 `retval=value` 选项，则会注入一个成功值。系统调用号会像 `error=` 选项一样被替换，但不是返回错误，而是将指定的成功 `value` 返回给调用进程。

    如果指定 `signal=sig` 选项，并给出符号值（如 `SIGSEGV`）或 1..`SIGRTMAX` 范围内的数值，则每次进入 `syscall_set` 指定的系统调用时都会投递该信号。

    如果指定 `delay_enter=delay` 或 `delay_exit=delay` 选项，则执行延迟注入：被跟踪进程分别在进入或退出系统调用时被延迟 `delay` 指定的时间段。`delay` 规格的格式在“时间规格格式说明”一节中描述。

    如果指定 `poke_enter=@argN=DATAN,@argM=DATAM...` 或 `poke_exit=@argN=DATAN,@argM=DATAM...` 选项，则系统调用参数 `argN` 和 `argM`（从 `arg1` 到 `arg7`）指向的被跟踪进程内存位置会被数据 `DATAN` 和 `DATAM` 覆盖（以十六进制格式指定；例如 `poke_enter=@arg1=0000DEAD0000BEEF`）。`poke_enter` 选项在系统调用进入时修改内存，`poke_exit` 则在系统调用退出时修改内存。

    注入动作是独立的。例如，仅指定 `signal=` 会投递信号而不改变系统调用结果或延迟它。类似地，仅指定 `error=` 会注入系统调用故障，而不添加信号或延迟。

    如果 `signal=sig` 选项与 `error=errno` 或 `retval=value` 一起指定，则会同时执行故障或成功注入以及信号投递。

    如果指定 `syscall=syscall` 选项，则会注入给定的 `syscall`，而不是默认的 `-1`。指定的 `syscall` 必须没有副作用；目前仅支持 `%pure` 集合中的系统调用。

    除非指定 `when=expr` 子表达式，否则会对 `syscall_set` 中每个系统调用的每次调用进行注入。

    子表达式格式为：

    ```sh
    first[..last][+[step]]
    ```

    数字 `first` 表示范围内的第一个调用编号，数字 `last` 表示范围内的最后一个调用编号，`step` 表示两个连续调用之间的步长。以下组合很有用：

    - `first`  
        对 `syscall_set` 中的每个系统调用，仅注入到调用编号 `first`。
    - `first..last`  
        对 `syscall_set` 中的每个系统调用，注入到从 `first` 到 `last`（含）的调用。
    - `first+`  
        对 `syscall_set` 中的每个系统调用，从编号 `first` 开始注入到每次调用。
    - `first+step`  
        对 `syscall_set` 中的每个系统调用，注入到编号 `first`、`first+step`、`first+step+step` 等调用。
    - `first..last+step`  
        同上，但仅考虑编号不超过 `last`（含）的调用。

    例如，要让每个第三个及后续 `chdir` 系统调用以 `ENOENT` 失败，使用 `--inject=chdir:error=ENOENT:when=3+`。

    数字 `first` 和 `step` 的有效范围是 1..65535，数字 `last` 的有效范围是 1..65534。

    一个注入表达式最多可包含一个故障或返回值规格（即 `error=` 或 `retval=`）和一个 `signal=` 规格。如果一个注入表达式包含多个 `when=` 规格，最后一个生效。

    受注入影响的系统调用计数按系统调用和按被跟踪进程进行。

    系统调用注入的规格可与其他系统调用过滤选项组合，例如 `-P /dev/urandom --inject=file:error=ENOENT`。

- `-e inject=args`  
    这等价于 `--inject=args`。

- `--fault=syscall_set[:error=errno][:when=expr]`  
    对指定的系统调用集合执行系统调用故障注入。

    这是更通用的 `--inject=` 选项的快捷方式，默认 `errno` 为 `ENOSYS`。

- `-e fault=args`  
    这等价于 `--fault=args`。

### 杂项

- 
    ```
    -d
    --debug
    ```
    在标准错误上显示 `strace` 自身的一些调试输出。

- `-F`  
    此选项已弃用。仅为向后兼容而保留，并可能在未来版本中移除。使用多个 `-F` 选项等价于单个 `-f`。如果与一个或多个 `-f` 选项一起使用，则此选项完全被忽略。

- 
    ```
    -h
    --help
    ```
    打印帮助摘要。

- `--seccomp-bpf`  
    尝试使用 seccomp-bpf（参见 `seccomp(2)`）使内核仅对正在跟踪的系统调用停止被跟踪进程。

    除非同时指定 `-f`/`--follow-forks`，否则此选项无效。`--seccomp-bpf` 与 `--syscall-limit` 和 `-b`/`--detach-on` 选项不兼容。它也不适用于使用 `-p`/`--attach` 选项附加的进程。

    尝试使用 seccomp-bpf 启用系统调用过滤可能因各种原因失败，例如要过滤的系统调用太多、seccomp API 不可用，或 `strace` 自身正在被跟踪。如果 seccomp-bpf 过滤器设置失败，`strace` 会照常继续，在每个系统调用上停止被跟踪进程。

    当 `--seccomp-bpf` 激活且未使用 `-p`/`--attach` 选项时，`--kill-on-exit` 选项也会被激活。

    注意，当被跟踪进程有另一个 seccomp 过滤器返回优先级高于 `SECCOMP_RET_TRACE` 的动作值时，`strace --seccomp-bpf` 将不会收到通知。也就是说，如果另一个 seccomp 过滤器例如禁用该系统调用或杀死被跟踪进程，则 `strace --seccomp-bpf` 完全不会知道该系统调用调用。

- `--tips[=[[id:]id],[[format:]format]]`  
    在退出前显示 `strace` 提示、技巧和调整建议。`id` 可以是非负整数，用于打印特定提示（注意：这些 ID 不保证稳定）。它也可以是 `random`（默认值），此时会打印随机提示。`format` 可以是以下之一：

    - `none`  
        不打印提示。可用于覆盖之前的设置。
    - `compact`  
        以刚好足以包含所有文本的大小打印提示。
    - `full`  
        以完整形式打印提示。

    默认值为 `id:random,format:compact`。

- 
    ```
    -V
    --version
    ```
    打印 `strace` 的版本号以及已启用的可选特性列表。多次使用此选项超过特定阈值会增加 der Strauss 意识。

### 时间规格格式说明

时间值指定为十进制浮点数（采用 `strtod(3)` 接受的格式），可选地后跟表示时间单位的后缀：`s`（秒）、`ms`（毫秒）、`us`（微秒）或 `ns`（纳秒）。如果未指定后缀，则值默认为微秒。

所述格式用于 `-O`、`--inject=delay_enter` 和 `--inject=delay_exit` 选项。

## 诊断

当 `command` 退出时，`strace` 以相同的退出状态退出。如果 `command` 被信号终止，`strace` 会以相同的信号终止自身，因此 `strace` 可用作对调用父进程透明的包装进程。注意，除非使用 `-D`，否则被跟踪进程与其父进程之间的父子关系（信号停止通知、`getppid(2)` 值等）不会被保留。

在不带 `command` 使用 `-p` 时，除非没有附加任何进程或跟踪期间发生意外错误，否则 `strace` 的退出状态为零。

## SETUID 安装

如果 `strace` 被安装为 setuid root，则调用用户将能够附加到并跟踪任何用户拥有的进程。此外，setuid 和 setgid 程序将以正确的有效特权执行和跟踪。由于这些能力应仅授予具有完整 root 特权的用户，因此仅当 `strace` 的使用限于此类受信任用户时，才适合将其安装为 setuid root。例如，可以安装一个特殊版本的 `strace`，模式为 `rwsr-x---`，用户为 `root`，组为 `trace`。在此配置中，只有属于 `trace` 组的受信任用户才能执行它。如果使用此特性，请记住还要为普通用户安装一个常规的非 setuid 版本的 `strace`。

## 多 personality 支持

在某些架构上，`strace` 可以解码使用与 `strace` 自身不同的应用程序二进制接口（ABI）的进程的系统调用。具体而言，除了解码本机 ABI 外，`strace` 还可以在以下架构上解码以下 ABI：

架构，支持的 ABI

- `x86_64`  
    `i386, x32 [1]; i386 [2]`
- `AArch64`  
    `ARM 32-bit EABI`
- `PowerPC 64-bit [3]`  
    `PowerPC 32-bit`
- `s390x`  
    `s390`
- `SPARC 64-bit`  
    `SPARC 32-bit`
- `TILE 64-bit`  
    `TILE 32-bit`

[1] 当 `strace` 构建为 x86_64 应用程序时  
[2] 当 `strace` 构建为 x32 应用程序时  
[3] 仅大端

此支持是可选的，取决于构建时生成和解析结构体定义的能力。请参阅 `strace -V` 命令的输出，以确定你的 `strace` 构建支持哪些 ABI。在此上下文中，“非本机”指与 `strace` 使用的 ABI 不同的 ABI：

- `m32-mpers`  
    `strace` 可以跟踪并正确解码非本机 32 位二进制程序。
- `no-m32-mpers`  
    `strace` 可以跟踪，但无法正确解码非本机 32 位二进制程序。
- `mx32-mpers`  
    `strace` 可以跟踪并正确解码非本机 32-on-64 位二进制程序。
- `no-mx32-mpers`  
    `strace` 可以跟踪，但无法正确解码非本机 32-on-64 位二进制程序。

如果输出既不包含 `m32-mpers` 也不包含 `no-m32-mpers`，表示解码非本机 32 位二进制程序的支持不适用于该架构。

同样，如果输出既不包含 `mx32-mpers` 也不包含 `no-mx32-mpers`，表示解码非本机 32-on-64 位二进制程序的支持不适用于该架构。

## 注意

使用共享库的系统在加载它们时通常会产生大量跟踪输出。

将系统调用的输入和输出视为跨用户/内核边界的数据流是有启发性的。由于用户空间和内核空间是分离且地址受保护的，有时可以使用输入和输出作为命题，对进程行为作出演绎推断。

某些情况下，系统调用会与文档描述的行为不同或名称不同。例如，底层的 `faccessat(2)` 系统调用没有 `flags` 参数，而 `setrlimit(2)` 库函数在现代（2.6.38+）内核上使用 `prlimit64(2)` 系统调用实现。这些差异是系统调用接口的正常特征，并由 C 库包装函数处理。

某些系统调用在不同架构和 personality 中具有不同名称。在这些情况下，系统调用过滤和打印使用与 `__NR_*` 内核宏匹配的名称，这些宏对应于被跟踪进程的架构和 personality。此一般规则有两个例外：`arm_fadvise64_64(2)` ARM 系统调用和 `xtensa_fadvise64_64(2)` Xtensa 系统调用会被过滤和打印为 `fadvise64_64(2)`。

在 x32 ABI 上，某些系统调用面向 64 位进程，但可通过设置 `__X32_SYSCALL_BIT` 标志从 x32 调用。当发生这种情况时，`strace` 会用 `#64` 后缀标示这些调用。一个例子是 `readv(2)`，它在 x86_64 上是系统调用号 19，而其不同的 x32 对应项是系统调用号 515。

在某些平台上，使用 `-p` 选项附加的进程可能会从不可重启的系统调用收到虚假的 `EINTR` 错误。如果进程不尝试重启调用，这可能对其产生不可预测的影响。理想情况下，所有系统调用都应在 `strace` 附加时重启，使附加对被跟踪进程不可见，但少数系统调用不会。可以说，此类行为的每个实例都是内核缺陷。

由于 `strace` 直接执行指定的 `command` 而不经过 shell，缺少 shebang 行（例如 `#!/bin/sh`）的脚本会以 `ENOEXEC` 错误失败，即使 shell 可以正确运行它们。建议手动提供 shell 作为 `command`，并将脚本作为其参数。

## BUGS

使用 `setuid` 位的程序在被跟踪时不具有有效用户 ID 特权。

被跟踪进程比未跟踪进程运行得更慢。可通过使用 `--seccomp-bpf` 选项减轻性能影响。

跟踪 `command` 时，其子进程可能在 `strace` 被中断信号（如 `CTRL-C`）终止后仍在运行。可通过使用 `--kill-on-exit` 选项，或以隐含 `--kill-on-exit` 的方式使用 `--seccomp-bpf` 选项来防止。

被跟踪进程可以在 `clone` 系统调用中使用 `CLONE_UNTRACED` 标志创建一个不被 `strace` 跟踪的子进程。这破坏了 `--seccomp-bpf` 选项的保证，因为该未跟踪子进程可能在 `strace` 终止后仍保留活动的 seccomp 过滤器。

## 历史

最初的 `strace` 由 Paul Kranenburg 为 SunOS 编写，并受其 `trace` 工具启发。SunOS 版本的 `strace` 被 Branko Lankester 移植到 Linux 并增强，他还编写了 Linux 内核支持。尽管 Paul 在 1992 年发布了 `strace` 2.5，但 Branko 的工作基于 Paul 1991 年的 `strace` 1.5 版本。

1993 年，Rick Sladkey 接手该项目。他将 SunOS 的 `strace` 2.5 与 Linux 版 `strace` 的第二个版本合并，添加了 SVR4 `truss(1)` 的许多特性，并产出了一个可同时在这两个平台上工作的 `strace` 版本。1994 年，Rick 将 `strace` 移植到 SVR4 和 Solaris，并编写了自动配置支持。1995 年，他将其移植到 Irix（并且厌倦了用第三人称写自己）。

从 1996 年开始，`strace` 由 Wichert Akkerman 维护。在其任期内，`strace` 开发迁移到 CVS；引入了对 FreeBSD 以及 Linux 上许多架构（包括 ARM、IA-64、MIPS、PA-RISC、PowerPC、s390、SPARC）的移植。

2002 年，`strace` 维护责任转移给 Roland McGrath。此后，`strace` 增加了对若干新 Linux 架构（AMD64、s390x、SuperH）的支持，对其中一些架构提供双架构支持，并在 Linux 上对系统调用解码器进行了大量添加和改进；在此期间，`strace` 开发迁移到 Git。

自 2009 年以来，`strace` 由 Dmitry Levin 积极维护。在此期间，`strace` 增加了对 AArch64、ARC、AVR32、Blackfin、C-SKY、LoongArch、Meta、Nios II、OpenRISC 1000、RISC-V、Tile/TileGx 和 Xtensa 架构的支持。2012 年，移除了对非 Linux 操作系统的未维护且明显损坏的支持。此外，2012 年 `strace` 增加了对路径跟踪和文件描述符路径解码的支持。2014 年，增加了栈回溯打印支持。2016 年，实现了系统调用篡改。

更多信息请参阅 `NEWS` 文件和 `strace` 仓库提交日志。

## 报告缺陷

`strace` 的问题应报告到 `strace` 邮件列表 ⟨mailto:strace-devel@lists.strace.io⟩。

## 另请参阅

`strace-log-merge(1)`、`ltrace(1)`、`perf-trace(1)`、`trace-cmd(1)`、`time(1)`、`ptrace(2)`、`seccomp(2)`、`syscall(2)`、`proc(5)`、`signal(7)`

`strace` 主页：<https://strace.io/>

## 作者

`strace` 贡献者的完整列表可在 `CREDITS` 文件中找到。

## COLOPHON

此页面是 `strace`（系统调用跟踪器）项目的一部分。项目信息可在 <http://strace.io/> 找到。如果对本手册页有缺陷报告，请发送到 `strace-devel@lists.sourceforge.net`。此页面从项目上游 Git 仓库 <https://github.com/strace/strace.git> 获取，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-07-15。）如果你发现此 HTML 版本页面存在渲染问题，或认为有更好或更新的页面来源，或对 COLOPHON 中的信息（该信息不属于原始手册页）有更正或改进，请发送邮件到 `man-pages@man7.org`。

```log
strace 7.1.0.62.c605d6          2026-06-25                      STRACE(1)
```